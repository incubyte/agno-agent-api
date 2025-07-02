"""
Free Geospatial Intelligence Tools for Location Intelligence Agent
Uses entirely free APIs and services for location-based health intelligence
"""

import requests
import json
import time
import logging
from typing import Dict, List, Optional, Tuple, Any
from urllib.parse import quote_plus
from datetime import datetime, timedelta
import re

try:
    from geopy.geocoders import Nominatim
    from geopy.distance import geodesic
    GEOPY_AVAILABLE = True
except ImportError:
    GEOPY_AVAILABLE = False

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FreeGeoIntelligenceTools:
    """
    Free geospatial intelligence tools using open-source APIs and services
    """
    
    def __init__(self, delay: float = 1.0):
        """
        Initialize geospatial intelligence tools
        
        Args:
            delay: Delay between API requests to be respectful
        """
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'LocationIntelligenceAgent/1.0 (Health Intelligence System)'
        })
        
        # Initialize geocoder if geopy is available
        if GEOPY_AVAILABLE:
            self.geocoder = Nominatim(user_agent="location_intelligence_agent")
        else:
            self.geocoder = None
            logger.warning("geopy not available, geocoding will be limited")
    
    def geocode_location(self, location_input: str) -> Dict[str, Any]:
        """
        Convert location input to coordinates and administrative boundaries
        
        Args:
            location_input: Address, city, coordinates, or region name
            
        Returns:
            Dict containing coordinates, address, and administrative data
        """
        try:
            # Check if input looks like coordinates
            if self._is_coordinate_pair(location_input):
                return self._parse_coordinates(location_input)
            
            # Use Nominatim for geocoding if available
            if self.geocoder:
                location = self.geocoder.geocode(location_input, exactly_one=True, addressdetails=True)
                if location:
                    return self._format_geocoding_result(location)
            
            # Fallback to manual parsing
            return self._fallback_location_parsing(location_input)
            
        except Exception as e:
            logger.error(f"Geocoding error for '{location_input}': {e}")
            return self._create_error_response(location_input, str(e))
    
    def _is_coordinate_pair(self, text: str) -> bool:
        """Check if text looks like lat,lon coordinates"""
        coord_pattern = r'^-?\d+\.?\d*\s*,\s*-?\d+\.?\d*$'
        return bool(re.match(coord_pattern, text.strip()))
    
    def _parse_coordinates(self, coord_text: str) -> Dict[str, Any]:
        """Parse coordinate string into structured data"""
        try:
            lat_str, lon_str = coord_text.split(',')
            latitude = float(lat_str.strip())
            longitude = float(lon_str.strip())
            
            # Reverse geocode if possible
            if self.geocoder:
                location = self.geocoder.reverse((latitude, longitude), exactly_one=True)
                if location:
                    address = location.address
                    admin_data = self._extract_admin_levels(location.raw.get('address', {}))
                else:
                    address = f"{latitude}, {longitude}"
                    admin_data = {}
            else:
                address = f"{latitude}, {longitude}"
                admin_data = {}
            
            return {
                'coordinates': {'latitude': latitude, 'longitude': longitude},
                'address_formatted': address,
                'administrative_levels': admin_data,
                'geocoding_confidence': 'high',
                'data_source': 'coordinate_input'
            }
            
        except Exception as e:
            logger.error(f"Error parsing coordinates '{coord_text}': {e}")
            return self._create_error_response(coord_text, str(e))
    
    def _format_geocoding_result(self, location) -> Dict[str, Any]:
        """Format Nominatim geocoding result"""
        try:
            address_parts = location.raw.get('address', {})
            admin_levels = self._extract_admin_levels(address_parts)
            
            return {
                'coordinates': {
                    'latitude': float(location.latitude),
                    'longitude': float(location.longitude)
                },
                'address_formatted': location.address,
                'administrative_levels': admin_levels,
                'geocoding_confidence': 'high',
                'data_source': 'nominatim',
                'place_id': location.raw.get('place_id'),
                'importance': location.raw.get('importance', 0)
            }
            
        except Exception as e:
            logger.error(f"Error formatting geocoding result: {e}")
            return self._create_error_response(str(location), str(e))
    
    def _extract_admin_levels(self, address_parts: Dict) -> Dict[str, str]:
        """Extract administrative boundary levels from address data"""
        admin_mapping = {
            'country': ['country', 'country_code'],
            'state_province': ['state', 'state_district', 'region'],
            'county_district': ['county', 'state_district', 'district'],
            'city': ['city', 'town', 'village', 'municipality'],
            'postal_code': ['postcode']
        }
        
        admin_levels = {}
        
        for level, keys in admin_mapping.items():
            for key in keys:
                if key in address_parts:
                    admin_levels[level] = address_parts[key]
                    break
        
        return admin_levels
    
    def _fallback_location_parsing(self, location_input: str) -> Dict[str, Any]:
        """Fallback location parsing when geocoding not available"""
        # Simple pattern matching for common location formats
        parts = location_input.split(',')
        
        admin_levels = {}
        if len(parts) >= 2:
            admin_levels['city'] = parts[0].strip()
            admin_levels['state_province'] = parts[1].strip()
            if len(parts) >= 3:
                admin_levels['country'] = parts[2].strip()
        
        return {
            'coordinates': {'latitude': None, 'longitude': None},
            'address_formatted': location_input,
            'administrative_levels': admin_levels,
            'geocoding_confidence': 'low',
            'data_source': 'fallback_parsing',
            'note': 'Coordinates not available, install geopy for full geocoding'
        }
    
    def _create_error_response(self, input_text: str, error_msg: str) -> Dict[str, Any]:
        """Create standardized error response"""
        return {
            'coordinates': {'latitude': None, 'longitude': None},
            'address_formatted': input_text,
            'administrative_levels': {},
            'geocoding_confidence': 'failed',
            'data_source': 'error',
            'error': error_msg
        }
    
    def calculate_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """
        Calculate distance between two points in kilometers
        
        Args:
            point1: (latitude, longitude)
            point2: (latitude, longitude)
            
        Returns:
            Distance in kilometers
        """
        try:
            if GEOPY_AVAILABLE:
                return geodesic(point1, point2).kilometers
            else:
                # Fallback haversine formula
                return self._haversine_distance(point1, point2)
        except Exception as e:
            logger.error(f"Distance calculation error: {e}")
            return 0.0
    
    def _haversine_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """Haversine distance formula as fallback"""
        import math
        
        lat1, lon1 = point1
        lat2, lon2 = point2
        
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Earth radius in kilometers
        r = 6371
        
        return c * r
    
    def find_nearby_locations(self, center: Tuple[float, float], locations: List[Dict], max_distance_km: float = 50) -> List[Dict]:
        """
        Find locations within specified distance of center point
        
        Args:
            center: (latitude, longitude) of center point
            locations: List of location dicts with 'latitude' and 'longitude' keys
            max_distance_km: Maximum distance in kilometers
            
        Returns:
            List of locations within distance, sorted by proximity
        """
        nearby = []
        
        for location in locations:
            try:
                if 'latitude' in location and 'longitude' in location:
                    if location['latitude'] and location['longitude']:
                        point = (location['latitude'], location['longitude'])
                        distance = self.calculate_distance(center, point)
                        
                        if distance <= max_distance_km:
                            location_copy = location.copy()
                            location_copy['distance_km'] = round(distance, 2)
                            nearby.append(location_copy)
            except Exception as e:
                logger.warning(f"Error calculating distance for location: {e}")
                continue
        
        # Sort by distance
        nearby.sort(key=lambda x: x['distance_km'])
        return nearby
    
    def get_administrative_context(self, admin_levels: Dict[str, str]) -> Dict[str, Any]:
        """
        Get health and demographic context for administrative area
        
        Args:
            admin_levels: Administrative boundary information
            
        Returns:
            Context information including population estimates and classifications
        """
        context = {
            'population_estimate': 'unknown',
            'urban_rural_classification': 'unknown',
            'health_jurisdiction': {},
            'demographic_notes': []
        }
        
        try:
            # Basic population estimates based on administrative level
            if 'city' in admin_levels:
                city = admin_levels['city'].lower()
                context['population_estimate'] = self._estimate_city_population(city)
                context['urban_rural_classification'] = 'urban'
            elif 'county_district' in admin_levels:
                context['urban_rural_classification'] = 'mixed'
                context['population_estimate'] = 'county_level'
            elif 'state_province' in admin_levels:
                context['urban_rural_classification'] = 'state_level'
                context['population_estimate'] = 'state_level'
            
            # Health jurisdiction information
            if 'country' in admin_levels:
                country = admin_levels['country']
                context['health_jurisdiction']['country'] = country
                context['health_jurisdiction']['health_authority'] = self._get_health_authority(country)
            
            if 'state_province' in admin_levels:
                state = admin_levels['state_province']
                context['health_jurisdiction']['state_province'] = state
                context['health_jurisdiction']['state_health_dept'] = f"{state} Department of Health"
            
        except Exception as e:
            logger.error(f"Error getting administrative context: {e}")
            context['error'] = str(e)
        
        return context
    
    def _estimate_city_population(self, city_name: str) -> str:
        """Simple city population estimation"""
        # This is a very basic estimation - in production you'd use a proper database
        major_cities = {
            'new york': 'large_metro',
            'los angeles': 'large_metro', 
            'chicago': 'large_metro',
            'houston': 'large_metro',
            'phoenix': 'large_metro',
            'philadelphia': 'large_metro',
            'san antonio': 'large_metro',
            'san diego': 'large_metro',
            'dallas': 'large_metro',
            'san jose': 'large_metro'
        }
        
        if city_name in major_cities:
            return 'large_metro_1M+'
        elif len(city_name) > 10:  # Rough heuristic
            return 'medium_city_100K+'
        else:
            return 'small_city_under_100K'
    
    def _get_health_authority(self, country: str) -> str:
        """Get primary health authority for country"""
        health_authorities = {
            'united states': 'CDC (Centers for Disease Control and Prevention)',
            'canada': 'Health Canada / Public Health Agency of Canada',
            'united kingdom': 'UK Health Security Agency',
            'australia': 'Department of Health',
            'germany': 'Robert Koch Institute',
            'france': 'Santé publique France',
            'india': 'Ministry of Health and Family Welfare',
            'china': 'National Health Commission',
            'japan': 'Ministry of Health, Labour and Welfare',
            'brazil': 'Ministry of Health',
        }
        
        country_lower = country.lower()
        return health_authorities.get(country_lower, f"{country} Ministry/Department of Health")


class FreeHealthDataSources:
    """
    Free health data source integrations for real-time intelligence
    """
    
    def __init__(self, delay: float = 1.0):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'LocationIntelligenceAgent/1.0 (Health Intelligence System)'
        })
        self.cache = {}  # Simple in-memory cache
        self.cache_ttl = 3600  # 1 hour cache
    
    def get_cdc_outbreak_data(self, location_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get CDC outbreak information relevant to location
        Uses free CDC data sources and news monitoring
        """
        try:
            time.sleep(self.delay)
            
            # Check cache first
            cache_key = f"cdc_outbreaks_{location_context.get('administrative_levels', {}).get('state_province', 'unknown')}"
            if self._is_cache_valid(cache_key):
                return self.cache[cache_key]['data']
            
            outbreaks = []
            
            # Search for CDC outbreak information
            state = location_context.get('administrative_levels', {}).get('state_province', '')
            country = location_context.get('administrative_levels', {}).get('country', '')
            
            if state and country.lower() in ['united states', 'usa', 'us']:
                # Search for state-specific outbreak information
                search_queries = [
                    f"CDC outbreak {state} current active",
                    f"disease surveillance {state} health department",
                    f"{state} public health alerts current"
                ]
                
                for query in search_queries:
                    outbreak_info = self._search_outbreak_news(query)
                    outbreaks.extend(outbreak_info)
            
            # Cache results
            self.cache[cache_key] = {
                'data': outbreaks,
                'timestamp': time.time()
            }
            
            return outbreaks
            
        except Exception as e:
            logger.error(f"Error fetching CDC outbreak data: {e}")
            return []
    
    def get_who_health_alerts(self, location_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get WHO health alerts relevant to location
        """
        try:
            time.sleep(self.delay)
            
            country = location_context.get('administrative_levels', {}).get('country', '')
            
            # Check cache
            cache_key = f"who_alerts_{country}"
            if self._is_cache_valid(cache_key):
                return self.cache[cache_key]['data']
            
            alerts = []
            
            if country:
                # Search for WHO alerts for country
                search_queries = [
                    f"WHO health alert {country} current",
                    f"World Health Organization {country} disease outbreak",
                    f"{country} travel health advisory WHO"
                ]
                
                for query in search_queries:
                    alert_info = self._search_health_news(query)
                    alerts.extend(alert_info)
            
            # Cache results
            self.cache[cache_key] = {
                'data': alerts,
                'timestamp': time.time()
            }
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error fetching WHO health alerts: {e}")
            return []
    
    def _search_outbreak_news(self, query: str) -> List[Dict[str, Any]]:
        """Search for outbreak news using DuckDuckGo"""
        try:
            # Use DuckDuckGo instant answers API
            encoded_query = quote_plus(query)
            url = f"https://api.duckduckgo.com/?q={encoded_query}&format=json&no_html=1"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            # Extract relevant information
            if data.get('Abstract'):
                results.append({
                    'type': 'outbreak_info',
                    'source': 'DuckDuckGo/CDC',
                    'summary': data['Abstract'][:500],
                    'url': data.get('AbstractURL', ''),
                    'last_updated': datetime.now().isoformat()
                })
            
            # Check related topics
            for topic in data.get('RelatedTopics', [])[:3]:
                if topic.get('Text'):
                    results.append({
                        'type': 'related_outbreak',
                        'source': 'DuckDuckGo',
                        'summary': topic['Text'][:300],
                        'url': topic.get('FirstURL', ''),
                        'last_updated': datetime.now().isoformat()
                    })
            
            return results
            
        except Exception as e:
            logger.warning(f"Error searching outbreak news for '{query}': {e}")
            return []
    
    def _search_health_news(self, query: str) -> List[Dict[str, Any]]:
        """Search for general health news"""
        try:
            # Simple news search using DuckDuckGo
            encoded_query = quote_plus(f"{query} news health")
            url = f"https://api.duckduckgo.com/?q={encoded_query}&format=json&no_html=1"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            if data.get('Abstract'):
                results.append({
                    'type': 'health_news',
                    'source': data.get('AbstractSource', 'News'),
                    'summary': data['Abstract'][:500],
                    'url': data.get('AbstractURL', ''),
                    'last_updated': datetime.now().isoformat()
                })
            
            return results
            
        except Exception as e:
            logger.warning(f"Error searching health news for '{query}': {e}")
            return []
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached data is still valid"""
        if cache_key not in self.cache:
            return False
        
        age = time.time() - self.cache[cache_key]['timestamp']
        return age < self.cache_ttl


# Example usage and testing
if __name__ == "__main__":
    # Test the tools
    geo_tools = FreeGeoIntelligenceTools()
    health_sources = FreeHealthDataSources()
    
    print("Testing geospatial tools...")
    result = geo_tools.geocode_location("Austin, Texas")
    print(f"Geocoding result: {result}")
    
    if result['coordinates']['latitude']:
        admin_context = geo_tools.get_administrative_context(result['administrative_levels'])
        print(f"Administrative context: {admin_context}")
        
        print("\nTesting health data sources...")
        outbreaks = health_sources.get_cdc_outbreak_data(result)
        print(f"Found {len(outbreaks)} outbreak-related items")
