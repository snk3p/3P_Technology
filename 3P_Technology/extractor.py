import json
from typing import List, Dict

def normalize_project_record(record: Dict) -> Dict:
    # compute delta and simple flags
    record['hour_delta'] = record.get('actual_hours', 0) - record.get('estimated_hours', 0)
    record['on_time'] = record['hour_delta'] <= 0
    return record

def load_projects(path: str) -> List[Dict]:
    with open(path, 'r') as f:
        projects = json.load(f)
    return [normalize_project_record(p) for p in projects]
