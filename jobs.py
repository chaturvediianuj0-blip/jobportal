# Job listing module
def list_jobs(): return []
# work in progress
def search_jobs(): pass
def search_jobs(keyword):
    jobs = list_jobs()
    return [j for j in jobs if keyword.lower() in str(j).lower()]
def sort_jobs(jobs, key='title'):
    return sorted(jobs, key=lambda j: j.get(key, ''))
def filter_by_location(location):
    return [j for j in list_jobs() if location in j]
