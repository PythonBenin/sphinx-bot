from celery import shared_task
from django.utils.timezone import now
from requests import ReadTimeout, ConnectionError

from repository.models import Repository


@shared_task
def launch():
    repositories = Repository.objects.filter(owner__is_active=True, issue_set__gt=0)[:100]
    for repository in repositories:
        connector = repository.owner.connector
        issues = repository.issue_set.filter(state='open')[:100]
        for issue in issues:
            reminds = issue.remind_set.filter(is_reminded=False, scheduled__lte=now())
            for remind in reminds:
                try:
                    response = connector.api.post(
                        f"repos/{repository.owner.username}/{repository.name}/issues/{issue.number}/comments",
                        data={
                            "body": f"Hi @{remind.author.username}, \n I am remind you like you said me"
                        })
                except (ConnectionError, ReadTimeout) as e:
                    continue
                if response.status_code == 201:
                    remind.is_reminded = True
                    remind.save()
    return True
