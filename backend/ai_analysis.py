import os
import google.generativeai as genai
from textblob import TextBlob  # Only kept as absolute fallback
import json
import re

# Initialize the Gemini API with your key
GEMINI_API_KEY = "AIzaSyA_amqgC7DYI5vgOsFLN6jrJa86wGWRV0A"
genai.configure(api_key=GEMINI_API_KEY)

def analyze_mood(story):
    """Analyze mood using Google Gemini API without predefined feedback templates."""
    
    if not story:
        return {"mood": "Unknown", "feedback": "No story provided."}

    try:
        # Try to get available models
        available_models = [m.name for m in genai.list_models()]
        print(f"Available Gemini models: {available_models}")
        
        # Filter for modern models - prioritizing the stable ones
        preferred_models = [
            "models/gemini-1.5-flash",
            "models/gemini-1.5-pro",
            "models/gemini-1.5-flash-latest",
            "models/gemini-2.0-flash",
            "models/gemini-2.0-pro-exp"
        ]
        
        # Try to use one of the preferred models
        model_name = None
        for preferred in preferred_models:
            if preferred in available_models:
                model_name = preferred
                break
                
        # If none of the preferred models are available, try any flash or pro model
        if not model_name:
            for model in available_models:
                if ("flash" in model.lower() or "pro" in model.lower()) and "vision" not in model.lower():
                    model_name = model
                    break
        
        if not model_name:
            # Emergency fallback
            print("No suitable Gemini model found. Using TextBlob as emergency fallback.")
            return textblob_emergency_fallback(story)
        
        print(f"Using Gemini model: {model_name}")
        # Configure the model
        model = genai.GenerativeModel(model_name)
        
        # Prompt focusing on direct mood classification and feedback generation
        prompt = f"""
        Analyze this text: "{story}"
        
        First, determine the primary emotion/mood (choose only ONE from: joy, sadness, anger, fear, surprise, disgust, neutral).
        
        Then create a personalized, compassionate response (1-2 sentences) directly addressing what the person wrote.
        Make your feedback empathetic, varied, and naturally conversational - like a supportive friend would respond.
        
        Return ONLY a valid JSON object with exactly this structure:
        {{"mood": "chosen_mood", "feedback": "your personalized response"}}
        
        IMPORTANT: Return raw JSON with no markdown formatting, code blocks, or additional text.
        """
        
        # Generate response from Gemini with specific configuration
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 200,
                "response_mime_type": "application/json"
            },
            safety_settings=[
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
        )
        
        # Get the raw response and log it
        raw_response = response.text.strip()
        print(f"Raw Gemini response: {raw_response}")
        
        # Extract JSON - improved handling
        try:
            # First attempt: Try direct parsing (if the response is already clean JSON)
            try:
                result = json.loads(raw_response)
                print("Successfully parsed JSON directly")
            except json.JSONDecodeError:
                # Clean the response and try again
                cleaned_json = clean_json_response(raw_response)
                print(f"Cleaned JSON: {cleaned_json}")
                result = json.loads(cleaned_json)
            
            # Validate the result has the required fields
            if 'mood' not in result or 'feedback' not in result:
                print(f"WARNING: Missing expected fields in Gemini response: {result}")
                return textblob_emergency_fallback(story)
            
            # Ensure mood is one of the valid moods
            valid_moods = ["joy", "sadness", "anger", "fear", "surprise", "disgust", "neutral"]
            if result['mood'].lower() not in valid_moods:
                closest_mood = get_closest_mood(result['mood'], valid_moods)
                result['mood'] = closest_mood
            
            print(f"AI analyzed mood: {result['mood']}, feedback: {result['feedback']}")
            return result
            
        except Exception as e:
            print(f"ERROR: Failed to process Gemini response: {str(e)}")
            return textblob_emergency_fallback(story)
            
    except Exception as e:
        print(f"ERROR: Gemini API error: {str(e)}")
        return textblob_emergency_fallback(story)

def clean_json_response(text):
    """Clean and extract JSON from the response text."""
    # Remove code block markers
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].strip()
    
    # Use regex to find JSON object pattern
    json_match = re.search(r'\{[\s\S]*\}', text)
    if json_match:
        text = json_match.group(0)
    
    # Replace single quotes with double quotes
    text = text.replace("'", '"')
    
    # Fix escape sequences
    text = text.replace('\\n', ' ')
    text = text.replace('\\"', '"')
    
    # Fix any trailing commas before closing braces
    text = re.sub(r',\s*}', '}', text)
    
    return text

def get_closest_mood(invalid_mood, valid_moods):
    """Map an invalid mood to the closest valid one."""
    invalid_mood = invalid_mood.lower()
    
    # Direct match
    for valid in valid_moods:
        if valid == invalid_mood:
            return valid
    
    # Substring match
    for valid in valid_moods:
        if valid in invalid_mood:
            return valid
    
    # Common synonyms
    mood_map = {
        "happy": "joy", "joyful": "joy", "excited": "joy", "elated": "joy", "pleased": "joy",
        "sad": "sadness", "unhappy": "sadness", "depressed": "sadness", "gloomy": "sadness",
        "angry": "anger", "mad": "anger", "furious": "anger", "irritated": "anger",
        "scared": "fear", "afraid": "fear", "anxious": "fear", "worried": "fear",
        "surprised": "surprise", "shocked": "surprise", "astonished": "surprise",
        "disgusted": "disgust", "repulsed": "disgust", "revolted": "disgust",
        "calm": "neutral", "ok": "neutral", "fine": "neutral", "balanced": "neutral"
    }
    
    for synonym, valid in mood_map.items():
        if synonym in invalid_mood:
            return valid
    
    # If all else fails, default to neutral
    return "neutral"

def textblob_emergency_fallback(story):
    """Absolute emergency fallback using TextBlob."""
    try:
        blob = TextBlob(story)
        sentiment = blob.sentiment.polarity
        
        # Determine basic mood from sentiment
        if sentiment > 0.3:
            mood = "joy"
        elif sentiment < -0.3:
            mood = "sadness"
        else:
            mood = "neutral"
            
        # Generate a very simple response
        return {
            "mood": mood,
            "feedback": "Thank you for sharing your thoughts with me."
        }
    except:
        return {"mood": "neutral", "feedback": "Thank you for sharing your thoughts with me."}
