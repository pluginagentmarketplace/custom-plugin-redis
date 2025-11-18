#!/usr/bin/env python3
"""
Developer Roadmap Analysis Plugin for Redis
Provides intelligent code recommendations and guidance based on curated roadmaps
"""

import json
import redis
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import timedelta


@dataclass
class RoadmapQuery:
    """Query object for roadmap searches"""
    domain: str
    category: str
    topic: Optional[str] = None
    search_term: Optional[str] = None


class RoadmapAnalysisPlugin:
    """
    Plugin for analyzing and providing guidance based on developer roadmaps.
    Uses Redis for caching and fast lookups.
    """

    def __init__(self, redis_host: str = "localhost", redis_port: int = 6379,
                 redis_db: int = 0, key_prefix: str = "roadmap:"):
        """
        Initialize the plugin with Redis connection

        Args:
            redis_host: Redis server host
            redis_port: Redis server port
            redis_db: Redis database number
            key_prefix: Prefix for all Redis keys
        """
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            decode_responses=True
        )
        self.key_prefix = key_prefix
        self.roadmaps = self._load_roadmap_schema()

    def _load_roadmap_schema(self) -> Dict[str, Any]:
        """Load roadmap schema from plugin_schema.json"""
        try:
            with open("/home/user/custom-plugin-redis/plugin_schema.json", "r") as f:
                schema = json.load(f)
                return schema.get("roadmaps", {})
        except FileNotFoundError:
            print("Warning: plugin_schema.json not found")
            return {}

    def cache_roadmap_data(self, roadmap_name: str, category: str, 
                          data: Any, ttl: int = 3600) -> bool:
        """
        Cache roadmap data in Redis

        Args:
            roadmap_name: Name of the roadmap
            category: Category within the roadmap
            data: Data to cache
            ttl: Time to live in seconds

        Returns:
            True if cached successfully
        """
        key = f"{self.key_prefix}{roadmap_name}:{category}"
        try:
            self.redis_client.setex(
                key,
                ttl,
                json.dumps(data) if not isinstance(data, str) else data
            )
            return True
        except Exception as e:
            print(f"Error caching data: {e}")
            return False

    def get_roadmap_data(self, roadmap_name: str, category: str) -> Optional[Any]:
        """
        Retrieve cached roadmap data

        Args:
            roadmap_name: Name of the roadmap
            category: Category within the roadmap

        Returns:
            Cached data or None if not found
        """
        key = f"{self.key_prefix}{roadmap_name}:{category}"
        try:
            data = self.redis_client.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            print(f"Error retrieving data: {e}")
            return None

    def get_security_principles(self, domain: str) -> Optional[List[str]]:
        """
        Get security principles for a given domain

        Args:
            domain: Domain name (cyber-security, golang, rust, etc.)

        Returns:
            List of security principles or None
        """
        cache_key = f"{self.key_prefix}{domain}:security"
        
        # Try cache first
        cached = self.redis_client.get(cache_key)
        if cached:
            return json.loads(cached)

        # Get from schema
        if domain in self.roadmaps:
            roadmap = self.roadmaps[domain]
            if "categories" in roadmap:
                principles = []
                
                # Extract security-related data
                if "security_principles" in roadmap["categories"]:
                    principles.extend(roadmap["categories"]["security_principles"])
                if "safety_guarantees" in roadmap["categories"]:
                    principles.extend(roadmap["categories"]["safety_guarantees"])
                
                # Cache for future use
                self.redis_client.setex(cache_key, 7200, json.dumps(principles))
                return principles

        return None

    def get_testing_methodologies(self, domain: str) -> Optional[Dict[str, List[str]]]:
        """
        Get testing methodologies for a given domain

        Args:
            domain: Domain name

        Returns:
            Dictionary of testing methodologies or None
        """
        cache_key = f"{self.key_prefix}{domain}:testing"
        
        # Try cache first
        cached = self.redis_client.get(cache_key)
        if cached:
            return json.loads(cached)

        # Get from schema
        if domain in self.roadmaps:
            roadmap = self.roadmaps[domain]
            if "categories" in roadmap:
                if "testing_methodologies" in roadmap["categories"]:
                    methodologies = roadmap["categories"]["testing_methodologies"]
                    # Cache for future use
                    self.redis_client.setex(
                        cache_key, 3600, json.dumps(methodologies)
                    )
                    return methodologies
                elif "testing" in roadmap["categories"]:
                    testing = roadmap["categories"]["testing"]
                    # Cache for future use
                    self.redis_client.setex(cache_key, 3600, json.dumps(testing))
                    return {"methodologies": testing}

        return None

    def get_best_practices(self, domain: str) -> Optional[List[str]]:
        """
        Get best practices for a given domain

        Args:
            domain: Domain name

        Returns:
            List of best practices or None
        """
        cache_key = f"{self.key_prefix}{domain}:best_practices"
        
        # Try cache first
        cached = self.redis_client.get(cache_key)
        if cached:
            return json.loads(cached)

        # Get from schema
        if domain in self.roadmaps:
            roadmap = self.roadmaps[domain]
            if "categories" in roadmap:
                if "best_practices" in roadmap["categories"]:
                    practices = roadmap["categories"]["best_practices"]
                    self.redis_client.setex(
                        cache_key, 7200, json.dumps(practices)
                    )
                    return practices

        return None

    def get_advanced_patterns(self, domain: str) -> Optional[Dict[str, Any]]:
        """
        Get advanced patterns for a given domain

        Args:
            domain: Domain name

        Returns:
            Dictionary of advanced patterns or None
        """
        cache_key = f"{self.key_prefix}{domain}:patterns"
        
        # Try cache first
        cached = self.redis_client.get(cache_key)
        if cached:
            return json.loads(cached)

        # Get from schema
        if domain in self.roadmaps:
            roadmap = self.roadmaps[domain]
            if "categories" in roadmap:
                patterns = {}
                
                if "advanced_patterns" in roadmap["categories"]:
                    patterns = roadmap["categories"]["advanced_patterns"]
                elif "design_patterns" in roadmap["categories"]:
                    patterns = roadmap["categories"]["design_patterns"]
                elif "advanced_features" in roadmap["categories"]:
                    patterns = roadmap["categories"]["advanced_features"]
                
                if patterns:
                    self.redis_client.setex(
                        cache_key, 7200, json.dumps(patterns)
                    )
                    return patterns

        return None

    def get_industry_standards(self, domain: str) -> Optional[List[str]]:
        """
        Get industry standards for a given domain

        Args:
            domain: Domain name

        Returns:
            List of industry standards or None
        """
        cache_key = f"{self.key_prefix}{domain}:standards"
        
        # Try cache first
        cached = self.redis_client.get(cache_key)
        if cached:
            return json.loads(cached)

        # Get from schema
        if domain in self.roadmaps:
            roadmap = self.roadmaps[domain]
            if "categories" in roadmap:
                if "industry_standards" in roadmap["categories"]:
                    standards = roadmap["categories"]["industry_standards"]
                    self.redis_client.setex(
                        cache_key, 7200, json.dumps(standards)
                    )
                    return standards
                elif "standards" in roadmap["categories"]:
                    standards = roadmap["categories"]["standards"]
                    self.redis_client.setex(
                        cache_key, 7200, json.dumps(standards)
                    )
                    return standards

        return None

    def get_roadmap_overview(self, domain: str) -> Optional[Dict[str, str]]:
        """
        Get overview information for a roadmap

        Args:
            domain: Domain name

        Returns:
            Dictionary with title and description
        """
        if domain in self.roadmaps:
            roadmap = self.roadmaps[domain]
            return {
                "title": roadmap.get("title", ""),
                "description": roadmap.get("description", "")
            }
        return None

    def search_by_topic(self, domain: str, search_term: str) -> Optional[List[str]]:
        """
        Search for topics containing a search term

        Args:
            domain: Domain name
            search_term: Term to search for

        Returns:
            List of matching topics or None
        """
        if domain not in self.roadmaps:
            return None

        roadmap = self.roadmaps[domain]
        matches = []
        search_lower = search_term.lower()

        # Search through all categories
        if "categories" in roadmap:
            for category, content in roadmap["categories"].items():
                matches.extend(self._search_in_content(content, search_lower))

        return matches if matches else None

    def _search_in_content(self, content: Any, search_term: str) -> List[str]:
        """
        Recursively search in content

        Args:
            content: Content to search in
            search_term: Term to search for

        Returns:
            List of matching items
        """
        matches = []
        
        if isinstance(content, list):
            matches.extend([
                item for item in content 
                if isinstance(item, str) and search_term in item.lower()
            ])
        elif isinstance(content, dict):
            for key, value in content.items():
                if search_term in key.lower():
                    matches.append(key)
                matches.extend(self._search_in_content(value, search_term))

        return matches

    def get_all_domains(self) -> List[str]:
        """Get list of all available domains"""
        return list(self.roadmaps.keys())

    def get_domain_categories(self, domain: str) -> Optional[List[str]]:
        """
        Get all categories for a domain

        Args:
            domain: Domain name

        Returns:
            List of category names or None
        """
        if domain in self.roadmaps:
            roadmap = self.roadmaps[domain]
            if "categories" in roadmap:
                return list(roadmap["categories"].keys())
        return None

    def health_check(self) -> bool:
        """Check if Redis connection is healthy"""
        try:
            self.redis_client.ping()
            return True
        except Exception as e:
            print(f"Redis health check failed: {e}")
            return False

    def clear_cache(self, pattern: str = "*") -> int:
        """
        Clear cached data matching pattern

        Args:
            pattern: Pattern to match (default: all)

        Returns:
            Number of keys deleted
        """
        try:
            keys = self.redis_client.keys(f"{self.key_prefix}{pattern}")
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except Exception as e:
            print(f"Error clearing cache: {e}")
            return 0


def main():
    """Example usage of the plugin"""
    
    # Initialize plugin
    plugin = RoadmapAnalysisPlugin()
    
    # Check connection
    if not plugin.health_check():
        print("Error: Cannot connect to Redis")
        return
    
    print("Developer Roadmap Analysis Plugin")
    print("=" * 50)
    
    # List all available domains
    domains = plugin.get_all_domains()
    print(f"\nAvailable Domains: {', '.join(domains)}\n")
    
    # Get information for each domain
    for domain in domains:
        overview = plugin.get_roadmap_overview(domain)
        if overview:
            print(f"\n{domain.upper()}")
            print(f"  Title: {overview['title']}")
            print(f"  Description: {overview['description']}")
            
            # Get security principles
            principles = plugin.get_security_principles(domain)
            if principles:
                print(f"  Security Principles: {len(principles)} items")
            
            # Get testing methodologies
            testing = plugin.get_testing_methodologies(domain)
            if testing:
                print(f"  Testing Methodologies: {len(testing)} types")
            
            # Get best practices
            practices = plugin.get_best_practices(domain)
            if practices:
                print(f"  Best Practices: {len(practices)} items")


if __name__ == "__main__":
    main()
