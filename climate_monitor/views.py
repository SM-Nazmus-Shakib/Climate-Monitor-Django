
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

@csrf_exempt
@require_http_methods(["POST"])
def chat_with_ai(request):
    """Simple rule-based chat responses for Bangladesh agriculture"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip().lower()
        
        if not user_message:
            return JsonResponse({
                'success': False,
                'error': 'Message is required'
            })
        response_text = get_agriculture_response(user_message)
        
        return JsonResponse({
            'success': True,
            'response': response_text
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid message format'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'Sorry, I couldn\'t process your request. Please try again.'
        })

def get_agriculture_response(user_message):
    """Generate agriculture-specific responses for Bangladesh farmers"""
    
    # Weather and climate responses
    if any(word in user_message for word in ['weather', 'rain', 'temperature', 'climate']):
        return "🌤️ Monitor weather forecasts daily using our weather section. Bangladesh weather can change quickly - prepare for both drought and flooding. Check rainfall patterns for proper irrigation timing."
    
    if any(word in user_message for word in ['monsoon', 'flood', 'flooding']):
        return "🌧️ Monsoon tips: Clean drainage channels, plant flood-resistant rice varieties like BRRI dhan51, elevate seed beds, and ensure proper water management to prevent crop damage."
    
    if any(word in user_message for word in ['drought', 'dry', 'water shortage']):
        return "☀️ Drought management: Use mulching to retain soil moisture, implement drip irrigation, plant drought-tolerant varieties, and harvest rainwater during monsoon for dry season use."
    
    # Rice cultivation (most important crop in Bangladesh)
    if any(word in user_message for word in ['rice', 'boro', 'aman', 'aus', 'dhan']):
        return "🌾 Rice cultivation: Use quality seeds like BRRI varieties, maintain 2-5cm water level, apply urea in 3 splits, watch for brown planthopper and blast disease. Plant Boro in Dec-Jan, Aman in Jun-Jul."
    
    # Other major crops
    if any(word in user_message for word in ['jute', 'pat']):
        return "🌿 Jute farming: Plant in March-April before monsoon, ensure good drainage, use 8-10 kg seeds per acre, and harvest before fiber becomes coarse (120-150 days after sowing)."
    
    if any(word in user_message for word in ['wheat', 'gom']):
        return "🌾 Wheat cultivation: Sow in November-December, use 120-140 kg seeds per acre, apply balanced fertilizer, and harvest before monsoon arrives in April-May."
    
    if any(word in user_message for word in ['potato', 'aloo']):
        return "🥔 Potato farming: Plant certified seeds in November-December, ensure well-drained soil, apply organic manure, and protect from late blight disease with proper fungicide spray."
    
    if any(word in user_message for word in ['tea', 'cha']):
        return "🍃 Tea cultivation: Prune during December-January, apply balanced fertilizer in split doses, ensure proper drainage, and harvest young shoots every 7-10 days during growing season."
    
    # Fertilizer and soil management
    if any(word in user_message for word in ['fertilizer', 'urea', 'tsp', 'mop', 'nutrients']):
        return "🌱 Fertilizer guide: Use soil testing for proper NPK ratios. Apply urea in 2-3 splits, TSP at planting, MOP at tillering. Organic fertilizers like compost improve soil health long-term."
    
    if any(word in user_message for word in ['soil', 'mati', 'ph', 'organic matter']):
        return "🌍 Soil health: Test soil pH (ideal 6.0-7.0), add organic matter through compost, practice crop rotation, avoid over-tillage, and use green manure crops to improve fertility."
    
    # Pest and disease management
    if any(word in user_message for word in ['pest', 'insect', 'bug', 'disease', 'fungus']):
        return "🐛 Pest control: Use IPM approach - resistant varieties, crop rotation, beneficial insects, pheromone traps. For rice: watch for brown planthopper, stem borer. Apply pesticides only when threshold reached."
    
    if any(word in user_message for word in ['brown planthopper', 'stem borer', 'blast']):
        return "⚠️ Major rice pests: Brown planthopper - use resistant varieties, avoid excessive nitrogen. Stem borer - use pheromone traps, release egg parasitoids. Blast disease - use resistant varieties, avoid late evening irrigation."
    
    # Irrigation and water management
    if any(word in user_message for word in ['irrigation', 'water', 'pani', 'watering']):
        return "💧 Water management: Use alternate wetting and drying for rice to save 25% water. Install drip irrigation for vegetables. Water early morning or evening to reduce evaporation."
    
    # Government schemes and support
    if any(word in user_message for word in ['government', 'loan', 'subsidy', 'support', 'scheme']):
        return "🏛️ Government support: Visit local Agricultural Extension Office for subsidized seeds, fertilizers, and training. Apply for agricultural loans through banks. Join farmer groups for better access to resources."
    
    # Seasonal advice
    if any(word in user_message for word in ['winter', 'rabi', 'sheet']):
        return "❄️ Winter crops (Rabi): Best time for wheat, potato, vegetables, mustard. Prepare land well, ensure irrigation facility, and protect from fog damage with proper spacing."
    
    if any(word in user_message for word in ['summer', 'grisho', 'kharif']):
        return "☀️ Summer crops (Kharif): Focus on rice, jute, sugarcane. Ensure adequate water supply, use heat-tolerant varieties, and prepare for monsoon planting."
    
    # Storage and post-harvest
    if any(word in user_message for word in ['storage', 'store', 'preserve', 'drying']):
        return "🏪 Post-harvest: Dry grains to 12-14% moisture, use proper storage containers, apply neem powder to prevent insects, and store in cool, dry places away from moisture."
    
    # Market and economics
    if any(word in user_message for word in ['price', 'market', 'sell', 'profit']):
        return "💰 Marketing tips: Check daily market prices, form farmer groups for better bargaining power, add value through processing, and diversify crops to reduce risk."
    
    # Technology and modern farming
    if any(word in user_message for word in ['technology', 'modern', 'app', 'digital']):
        return "📱 Modern farming: Use weather apps for forecasts, soil testing apps, market price apps. Consider mechanization for larger farms and precision agriculture techniques."
    
    # Default response for unmatched queries
    return "🌾 I'm here to help with Bangladesh agriculture! Ask me about rice cultivation, weather advice, irrigation, fertilizers, pest control, or any farming challenges you're facing."

# If you have existing views, make sure to keep them and just add the above functions