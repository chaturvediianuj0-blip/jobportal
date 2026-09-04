# Job listing module
def list_jobs(): return []
# work in progress
def search_jobs(): pass
def search_jobs(keyword):
    return [job for job in list_jobs() if keyword in job]
