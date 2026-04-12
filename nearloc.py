import numpy as np
import math

class nnear:

    def find_nearest_by_location(self, docs, user_id, radius=10):
        # docs is a list of dictionaries
        if not docs:
            return []
            
        # 1. Extract locations and find target
        target_loc = None
        locations = []
        valid_indices = []
        
        for i, doc in enumerate(docs):
            if doc['user'] == user_id:
                target_loc = doc['location']
            
            # Ensure valid location
            loc = doc.get('location')
            if loc and isinstance(loc, (list, tuple)) and len(loc) >= 2:
               locations.append([float(loc[0]), float(loc[1])])
               valid_indices.append(i)
        
        if not target_loc:
            return []
            
        if not locations:
            return []
            
        # Convert to numpy array for vectorization
        loc_array = np.array(locations)
        target_arr = np.array([float(target_loc[0]), float(target_loc[1])])
        
        # Vectorized Haversine
        R = 6371.0
        
        lat1 = np.radians(target_arr[0])
        lon1 = np.radians(target_arr[1])
        lat2 = np.radians(loc_array[:, 0])
        lon2 = np.radians(loc_array[:, 1])
        
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        
        a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        
        distances = R * c
        
        neighbors = []
        for i, dist in enumerate(distances):
            if dist <= radius:
                # Map back to original doc index
                original_idx = valid_indices[i]
                doc = docs[original_idx]
                
                # Skip user themselves (Wait, we need them for matching.py to calculate features!)
                # if doc['user'] == user_id:
                #    continue
                    
                neighbors.append({
                    'user': doc['user'],
                    'Name': doc['Name'],
                    'Distance': float(dist),
                    'Hobbies': doc['Hobbies'], 
                    'Budget': doc['Budget'],
                    'location': doc['location'], 
                    'Is_Vegetarian': doc['Is_Vegetarian'],
                    'mobile': doc['mobile'],
                    'image': doc.get('image', '')
                })
        
        # Sort by distance
        neighbors.sort(key=lambda x: x['Distance'])
            
        return neighbors