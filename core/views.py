from django.shortcuts import render
from .models import Planet, Recruit, Sith, TestTrials, Questions, Answers, DiscipleTeacher
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from .forms import RecruitCreateForm
from django.db import IntegrityError, models
from django.core.mail import send_mail
from .signals import LimitNumberRecordsError


from smtplib import SMTPException

from random import randint


class FormSelectSithRecruitView(View):

    def get(self, request):
        return render(request, 'select_sith_recruit.html', {})


class FormCreateRecruitView(View):

    def get(self, request):
        form = RecruitCreateForm()
        return render(request, 'create_recruit_form.html', {'form': form})


class FormSelectSithView(View):

    def get(self, request):

        siths = Sith.objects.annotate(count_disciples=models.Count('disciples'))
        all_siths = []
        more_than_one_siths = []
        for sith in siths.values():
            all_siths.append((sith['id'], sith['name'], sith['planet_of_learning_id'], sith['count_disciples']))
            if sith['count_disciples'] > 1:
                more_than_one_siths.append((sith['id'], sith['name'],
                                            sith['planet_of_learning_id'], sith['count_disciples']))
        context = {'siths': all_siths, 'more_than_one_siths': more_than_one_siths}
        return render(request, 'select_sith_form.html', context)


class FormSaveRecruitTestTrialView(View):
    # questions generator
    def __generate_questions(self):
        ordens = TestTrials.objects.values('orden_code')
        len_ordens = ordens.count()
        ind = randint(0, len_ordens - 1)
        orden_code = ordens[ind]['orden_code']
        ttrials = TestTrials.objects.get(orden_code=orden_code)
        query_set_questions = Questions.objects.filter(test_trial=ttrials)

        quests = []
        for q in query_set_questions.values():
            quests.append((q['id'], q['question']))
        return quests

    def post(self, request):
        form = RecruitCreateForm(request.POST)
        if form.is_valid():
            context = form.cleaned_data

            name = context['name']
            age = context['age']
            email = context['email']
            planet_habitat = context['planet_habitat']
            try:
                planet = Planet.objects.get(pk=planet_habitat)
                try:
                    recruit = Recruit.objects.get(name=name, age=age, email=email, planet_habitat=planet)
                except ObjectDoesNotExist:
                    try:
                        recruit = Recruit.objects.create(name=name, age=age, email=email, planet_habitat=planet)
                    except IntegrityError as exc:
                        return render(request, 'error.html', {'error': f'Пользователь с email: {email} уже существует!'})

                context = {'name': name, 'email': email}

                request.session['recruit_id'] = recruit.pk
                answers = Answers.objects.filter(recruit=recruit)

                if answers.count() == 0:
                    quests = self.__generate_questions()
                    context['quests'] = quests
                    request.session['questions'] = quests
                    return render(request, 'test_trial.html', context=context)
                else:
                    pairs_q_a = []
                    for question_answer in answers.values('quest__question', 'answer'):
                        pairs_q_a.append((question_answer['quest__question'], question_answer['answer']))
                    context['pairs_q_a'] = pairs_q_a
                    return render(request, 'test_trial_done.html', context=context)

            except ObjectDoesNotExist as exc:
                return render(request, 'error.html', {'error': f'Планеты {planet_habitat} нет в базе ({exc.args[0]})'})

        else:
            return render(request, 'error.html', {'error': form.errors})


class FormRecruitPostAnswersView(View):

    def post(self, request):
        recruit_id = request.session['recruit_id']
        recruit = Recruit.objects.get(pk=recruit_id)

        answers = Answers.objects.filter(recruit=recruit)
        if answers.count() == 0:
            quests = request.session['questions']

            for quest in quests:
                ans = Answers(quest=Questions.objects.get(id=quest[0]), answer=request.POST[str(quest[0])])
                ans.save()
                ans.recruit.add(recruit)
            return render(request, 'select_sith_recruit.html', {})
        else:
            pairs_q_a = []
            for question_answer in answers.values('quest__question', 'answer'):
                pairs_q_a.append((question_answer['quest__question'], question_answer['answer']))
            context = {'name': recruit.name, 'email': recruit.email}
            context['pairs_q_a'] = pairs_q_a
            return render(request, 'test_trial_done.html', context=context)


class FormSithSelectRecruitView(View):

    def post(self, request):

        sith_id = request.POST['selected_sith']
        request.session['sith_id'] = sith_id

        sith = Sith.objects.get(pk=sith_id)
        recruits = Answers.objects.filter(recruit__teacher__isnull=True,
                                          recruit__planet_habitat=sith.planet_of_learning).distinct(). \
            values('recruit__name', 'recruit__email', 'recruit__planet_habitat')

        if recruits.count() != 0:
            list_freedom_recruits = []
            for r in recruits:
                list_freedom_recruits.append((r['recruit__name'], r['recruit__email'], r['recruit__planet_habitat']))
            return render(request, 'select_sith_recruit_form.html', context={'recruits': list_freedom_recruits})
        else:
            return render(request, 'error.html', {'error': 'Нет свободных рекрутов'})


class FormMakeHandShadowView(View):
    def post(self, request):
        recruit_id = request.session['sith_selected_recruit']
        sith_id = request.session['sith_id']

        #if DiscipleTeacher.objects.filter(teacher=sith_id).count() < 3:
        try:
            recruit = Recruit.objects.get(pk=recruit_id)
            if DiscipleTeacher.objects.filter(disciple=recruit).count() == 0:
                sith = Sith.objects.get(pk=sith_id)
                DiscipleTeacher.objects.create(disciple=recruit, teacher=sith)
                try:
                    send_mail('The purpose of hand shadows', f'You are appointed by the shadow hand to {sith.name}',
                            'recruitingService@yandex.ru', recipient_list=[recruit.email], fail_silently=False)
                except SMTPException:
                    pass
                return render(request, 'select_sith_recruit.html', {})
            else:
                return render(request, 'error.html', {'error': 'Рекрут уже назначен рукой тени!'})
        except LimitNumberRecordsError:
            return render(request, 'error.html', {'error': 'У ситха уже 3 руки тени!'})


class FormShowAnswersView(View):
    def post(self, request):
        selected_recruit = request.POST['selected_recruit']
        request.session['sith_selected_recruit'] = selected_recruit
        recruit = Recruit.objects.get(pk=selected_recruit)

        answers = Answers.objects.filter(recruit=recruit)
        pairs_q_a = []
        for question_answer in answers.values('quest__question', 'answer'):
            pairs_q_a.append((question_answer['quest__question'], question_answer['answer']))
        context = {'name': recruit.name, 'email': recruit.email}
        context['pairs_q_a'] = pairs_q_a
        return render(request, 'select_recruit.html', context=context)



