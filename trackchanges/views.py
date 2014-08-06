import logging
#from django.contrib.auth.decorators import login_required
#from django.shortcuts import render_to_response
from openassessment.assessment.api.peer import get_assessments
#from submissions.api import SubmissionRequestError, get_submissions
import json
from django.http import HttpResponse
from trackchanges import models
from django.core import serializers

log = logging.getLogger(__name__)


#@login_required()
def get_change_tracker_for_assessment(request, assessmentworkflow_uuid):
    #student_item_dict = dict(
    #    course_id=course_id,
    #    student_id=student_id,
    #    item_id=item_id,
    #)
    #context = dict(**student_item_dict)
    #try:
    #    submissions = get_submissions(student_item_dict)
    #    evaluations = []
    #    for submission in submissions:
    #        submission_evaluations = get_assessments(submission["uuid"])
    #        for evaluation in submission_evaluations:
    #            evaluation["submission_uuid"] = submission["uuid"]
    #            evaluations.append(evaluation)
    #
    #    context["evaluations"] = evaluations
    #
    #except SubmissionRequestError:
    #    context["error"] = "The specified student item was not found."
    
    #data = models.ChangeTracker.objects.get(assessmentworkflow_uuid = assessmentworkflow_uuid).values()
    data = list(models.ChangeTracker.objects.all().values())

    #return render_to_response('evaluations.html', context)
    
    return HttpResponse(json.dumps(data))
