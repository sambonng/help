from core.models import ApprovalUnit


def notice(request):
    if request.user.is_authenticated():
        approval_count = ApprovalUnit.objects.filter(user=request.user,is_completed=False).count()

        return {
            'approval_count': approval_count,
        }
    return {

    }
