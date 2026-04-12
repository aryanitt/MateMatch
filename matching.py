import numpy as np


class model:
    def calculate_budget_similarity(self, budget1, budget2):
        """Calculate budget similarity as percentage (0-100)"""
        max_budget = max(budget1, budget2)
        if max_budget == 0:
            return 100.0
        
        difference = abs(budget1 - budget2)
        similarity = (1 - (difference / max_budget)) * 100
        return max(0, min(100, similarity))
    
    def calculate_hobby_overlap(self, hobbies1, hobbies2):
        """Calculate Jaccard similarity for hobbies (0-100)"""
        # Parse hobbies
        h1_set = set([h.strip().lower() for h in str(hobbies1).replace(',', ' ').split() if h.strip()])
        h2_set = set([h.strip().lower() for h in str(hobbies2).replace(',', ' ').split() if h.strip()])
        
        if not h1_set and not h2_set:
            return 50.0  # Both empty - neutral
        if not h1_set or not h2_set:
            return 0.0   # One empty - no overlap
        
        intersection = len(h1_set & h2_set)
        union = len(h1_set | h2_set)
        
        if union == 0:
            return 0.0
        
        return (intersection / union) * 100
    
    def calculate_diet_match(self, diet1, diet2):
        """Calculate diet compatibility (0 or 100)"""
        d1 = str(diet1).lower() == 'true'
        d2 = str(diet2).lower() == 'true'
        return 100.0 if d1 == d2 else 0.0
    
    def calculate_distance_score(self, distance_km):
        """Convert distance to score (0-100), closer = higher score"""
        # Within 1km = 100%, 10km = 0%, linear decay
        if distance_km <= 0:
            return 100.0
        if distance_km >= 10:
            return 0.0
        return (1 - (distance_km / 10)) * 100
    
    def calculate_match_score(self, user1, user2):
        """Calculate overall match score using weighted components"""
        # Component weights (must sum to 1.0)
        W_BUDGET = 0.35
        W_DIET = 0.25
        W_HOBBIES = 0.20
        W_DISTANCE = 0.20
        
        # Calculate individual scores
        budget_score = self.calculate_budget_similarity(user1['Budget'], user2['Budget'])
        diet_score = self.calculate_diet_match(user1['Is_Vegetarian'], user2['Is_Vegetarian'])
        hobby_score = self.calculate_hobby_overlap(user1['Hobbies'], user2['Hobbies'])
        distance_score = self.calculate_distance_score(user2.get('Distance', 0))
        
        # Weighted average
        total_score = (
            budget_score * W_BUDGET +
            diet_score * W_DIET +
            hobby_score * W_HOBBIES +
            distance_score * W_DISTANCE
        )
        
        return {
            'total': round(total_score, 1),
            'budget': round(budget_score, 1),
            'diet': round(diet_score, 1),
            'hobbies': round(hobby_score, 1),
            'distance': round(distance_score, 1)
        }
    
    def find_nearest_neighbors(self, user_id, all_users_data, k=10, min_match_threshold=30):
        """Find best matches using component-based scoring"""
        # Find target user
        target_user = None
        for u in all_users_data:
            if u['user'] == user_id:
                target_user = u
                break
        
        if not target_user:
            return []
        
        # Calculate match scores for all other users
        matches = []
        
        for candidate in all_users_data:
            # Skip self
            if candidate['user'] == user_id:
                continue
            
            # Calculate match score
            scores = self.calculate_match_score(target_user, candidate)
            
            # Filter by minimum threshold
            if scores['total'] < min_match_threshold:
                continue
            
            # Get location - just use coordinates, no slow API call
            loc = candidate.get('location')
            if isinstance(loc, (list, tuple)) and len(loc) >= 2:
                location_str = f"{loc[0]:.4f}, {loc[1]:.4f}"
            else:
                location_str = "Unknown"
            
            # Format diet preference
            is_veg = "Veg" if str(candidate.get('Is_Vegetarian', '')).lower() == 'true' else "Non-Veg"
            
            matches.append({
                'user': candidate['user'],
                'Name': candidate['Name'],
                'Matching': f"{int(scores['total'])}%",
                'MatchScore': scores['total'],  # For sorting
                'Distance': candidate.get('Distance', 0),
                'location': location_str,  # Coordinates instead of address
                'mobile': candidate['mobile'],
                'image': candidate.get('image', ''),
                'Budget': candidate['Budget'],
                'Hobbies': candidate['Hobbies'],
                'Is_Vegetarian': is_veg,
                # Component scores for debugging
                'budget_match': f"{int(scores['budget'])}%",
                'diet_match': f"{int(scores['diet'])}%",
                'hobby_match': f"{int(scores['hobbies'])}%",
                'distance_match': f"{int(scores['distance'])}%"
            })
        
        # Sort by match score (highest first)
        matches.sort(key=lambda x: x['MatchScore'], reverse=True)
        
        # Remove internal sorting field and return top k
        for match in matches:
            del match['MatchScore']
        
        return matches[:k]

    
    def fit_it(self, selected_user_id, nearby):
        """Main entry point for matching algorithm"""
        if not nearby:
            return []
        
        # Use the new component-based matching
        return self.find_nearest_neighbors(selected_user_id, nearby, k=10, min_match_threshold=30)