class Project:
    def __init__(self, id, name, description, version, repo_url, documentation, environments, requirements):
        self.id = id
        self.name = name
        self.description = description
        self.version = version
        self.repo_url = repo_url
        self.documentation = documentation
        self.environments = environments
        self.requirements = requirements
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "repo_url": self.repo_url
        }

class Environment:
    def __init__(self, name, version, last_deploy):
        self.name = name
        self.version = version
        self.last_deploy = last_deploy

class Documentation:
    def __init__(self, title, version, last_update):
        self.title = title
        self.version = version
        self.last_update = last_update