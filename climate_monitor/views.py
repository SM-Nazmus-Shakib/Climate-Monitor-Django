import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.conf import settings
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
import os
import logging

logger = logging.getLogger(__name__)

def get_agriculture_system_prompt():
    """System prompt for agriculture assistant"""
    return """You are an expert agriculture assistant for Bangladesh farmers. 

Provide practical advice on:
- Rice, wheat, potato cultivation
- Fertilizers (Urea, TSP, MOP amounts)
- Weather-based farming decisions
- Pest and disease management
- Market timing and prices

Keep responses under 200 words, use simple language, and include specific amounts/timing when relevant. You can respond in English or basic Bangla if needed."""

def try_github_ai(user_message):
    """Try to use GitHub AI API"""
    try:
        system_prompt = get_agriculture_system_prompt()
        
        endpoint = settings.GITHUB_AI_ENDPOINT
        model = settings.GITHUB_AI_MODEL
        token = settings.GITHUB_TOKEN
        
        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(token),
        )

        response = client.complete(
            messages=[
                SystemMessage(system_prompt),
                UserMessage(user_message),
            ],
            temperature=0.7,
            top_p=1.0,
            max_tokens=500,
            model=model
        )

        return response.choices[0].message.content
                
    except Exception as e:
        logger.error(f"GitHub AI API error: {str(e)}")
        return None

def try_local_ai(user_message):
    """Simple rule-based AI for common questions"""
    message_lower = user_message.lower()
    
    # Rice-related questions
    if any(word in message_lower for word in ['rice', 'ধান', 'paddy']):
        if 'fertilizer' in message_lower or 'urea' in message_lower or 'সার' in message_lower:
            return """For rice cultivation in Bangladesh:
• **Urea**: 180-200 kg per hectare (split into 3 applications)
• **TSP**: 90-100 kg per hectare (apply during final land preparation)
• **MOP**: 70-80 kg per hectare (apply during final land preparation)
• **Zinc**: 5-10 kg per hectare (if zinc deficiency is observed)

Apply first urea dose 15-20 days after transplanting, second dose at 35-40 days, and third dose at 55-60 days."""
        
        elif 'plant' in message_lower or 'চারা' in message_lower or 'সময়' in message_lower:
            return """Rice planting seasons in Bangladesh:
• **Aman rice**: Transplant June-July, harvest November-December
• **Boro rice**: Transplant January-February, harvest April-May
• **Aus rice**: Transplant March-April, harvest July-August

Ideal age for transplanting: 30-35 days for Aman, 40-45 days for Boro."""
        
        elif 'disease' in message_lower or 'রোগ' in message_lower:
            return """Common rice diseases in Bangladesh:
• **Blast**: Use resistant varieties like BRRI dhan49, BRRI dhan52
• **Bacterial leaf blight**: Avoid excessive nitrogen, use balanced fertilization
• **Sheath blight**: Maintain proper plant spacing, avoid water stagnation

For severe infections, consult with local agriculture office for appropriate fungicides."""
    
    # Wheat-related questions
    elif any(word in message_lower for word in ['wheat', 'গম']):
        return """Wheat cultivation in Bangladesh:
• **Planting time**: November is ideal
• **Fertilizer**: 120-150 kg Urea, 100-120 kg TSP, 80-100 kg MOP per hectare
• **Irrigation**: 3-4 irrigations needed (crown root, late tillering, flowering, grain filling stages)
• **Popular varieties**: BARI Gom 25, BARI Gom 26, BARI Gom 27

Harvest when grains are hard and moisture content is around 20-25%."""
    
    # Potato-related questions
    elif any(word in message_lower for word in ['potato', 'আলু']):
        return """Potato cultivation tips:
• **Planting time**: October to November
• **Seed rate**: 1500-1800 kg per hectare
• **Fertilizer**: 250-300 kg Urea, 180-200 kg TSP, 200-250 kg MOP per hectare
• **Harvest**: 90-100 days after planting

Store potatoes in cool, dark, well-ventilated place to prevent greening."""
    
    # Weather-related questions
    elif any(word in message_lower for word in ['weather', 'আবহাওয়া', 'rain', 'বৃষ্টি']):
        return """Weather considerations for farming in Bangladesh:
• **Monsoon (June-September)**: Ideal for Aman rice, but watch for flooding
• **Winter (November-February)**: Good for wheat, potato, vegetables
• **Summer (March-May)**: Suitable for Aus rice, mango, jackfruit

Check daily weather forecasts before applying pesticides or fertilizers."""
    
    return None

def get_fallback_response(message):
    """Enhanced fallback response"""
    local_ai_response = try_local_ai(message)
    if local_ai_response:
        return local_ai_response
    
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['rice', 'ধান']):
        return """🌾 **Rice Farming Tips:**
• **Aman**: Plant June-July, harvest Nov-Dec
• **Boro**: Plant Dec-Jan, harvest April-May
• **Fertilizer**: 80-100kg Urea + 40kg TSP per acre
• **Water**: Keep 2-3cm depth in field
• **Varieties**: BRRI dhan28, BRRI dhan29

Ask about specific rice problems!"""
    
    elif any(word in message_lower for word in ['wheat', 'গম']):
        return """🌾 **Wheat Cultivation:**
• **Season**: Plant Nov-Dec, harvest March-April
• **Fertilizer**: 60-80kg Urea + 40kg TSP per acre
• **Irrigation**: 3-4 times during growth
• **Varieties**: BARI Gom-25, BARI Gom-26

Need help with wheat diseases or timing?"""
    
    elif any(word in message_lower for word in ['potato', 'আলু']):
        return """🥔 **Potato Growing:**
• **Season**: Plant Nov-Dec, harvest Feb-March
• **Fertilizer**: 100kg Urea + 60kg TSP + 80kg MOP per acre
• **Disease**: Prevent late blight with good drainage
• **Storage**: Cool, dark place for better prices

Ask about potato diseases or market timing!"""
    
    else:
        return """🌱 **Agriculture Assistant Ready!**

I can help with:
• Rice, wheat, potato farming
• Fertilizer recommendations  
• Disease prevention
• Weather advice
• Market information

**Ask specific questions like:**
• "How much urea for rice?"
• "When to plant wheat?"
• "How to prevent rice blast?"

What farming question do you have?"""


@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            user_message = data.get("message", "").strip()

            # Input validation
            if not user_message:
                return JsonResponse({"success": False, "error": "Please enter a message."})
            
            if len(user_message) > 200:
                return JsonResponse({"success": False, "error": "Message too long. Please keep under 200 characters."})

            
            github_ai_response = try_github_ai(user_message)
            if github_ai_response:
                return JsonResponse({
                    "success": True, 
                    "response": github_ai_response,
                    "source": "github_ai"
                })

            
            fallback_response = get_fallback_response(user_message)
            return JsonResponse({
                "success": True, 
                "response": fallback_response,
                "source": "fallback"
            })

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid message format."})
        except Exception as e:
            logger.error(f"Chat view error: {str(e)}")
            return JsonResponse({"success": False, "error": "Something went wrong. Please try again."})
    
    return JsonResponse({"success": False, "error": "Invalid request method."})

def home(request):
    """Home view"""
    return render(request, 'home.html')