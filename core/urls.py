from django.urls import path, re_path

from .views import FormSelectSithRecruitView, FormCreateRecruitView, FormSelectSithView, FormRecruitPostAnswersView,\
    FormSaveRecruitTestTrialView, FormSithSelectRecruitView, FormMakeHandShadowView, FormShowAnswersView

app_name = 'Recruit'

urlpatterns = [
    path('select_sith_or_recruit/', FormSelectSithRecruitView.as_view(), name='recruit_select_sith_or_recruit'),
    re_path(r'.*/create_recruit/', FormCreateRecruitView.as_view()),
    re_path(r'.*select_sith/', FormSelectSithView.as_view()),
    re_path(r'.*/save_recruit_get_test_trial/', FormSaveRecruitTestTrialView.as_view(),
            name='recruit_get_test_trial'),
    re_path(r'post_answers/', FormRecruitPostAnswersView.as_view(), name='recruit_post_answers'),
    re_path(r'.*/sith_select_recruit/', FormSithSelectRecruitView.as_view(), name='recruit_sith_select_recruit'),
    re_path(r'.*/make_hand_shadows/', FormMakeHandShadowView.as_view(), name='recruit_make_hand_shadows'),
    re_path(r'.*/show_recruit_answers/', FormShowAnswersView.as_view(), name='recruit_show_recruit_answers'),
]
