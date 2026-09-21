import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from .models import User, MuscleGroup, Workout, WorkoutStats
from .forms import UserForm, MuscleGroupForm, WorkoutForm


def to_dict(obj, fields):
    result = {}
    for f in fields:
        value = getattr(obj, f)
        result[f] = str(value) if value is not None else None
    return result


def parse_body(request):
    try:
        return json.loads(request.body)
    except:
        return {}


@method_decorator(require_http_methods(["GET", "POST"]), name='dispatch')
class UserListView(View):
    def get(self, request):
        users = User.objects.all()
        return JsonResponse([to_dict(u, ['id', 'name', 'created_at']) for u in users], safe=False)

    def post(self, request):
        form = UserForm(parse_body(request))
        if not form.is_valid():
            return JsonResponse({"errors": form.errors}, status=400)
        u = form.save()
        return JsonResponse(to_dict(u, ['id', 'name', 'created_at']), status=201)


@method_decorator(require_http_methods(["GET", "PUT", "DELETE"]), name='dispatch')
class UserDetailView(View):
    def get(self, request, user_id):
        try:
            u = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "Не найден"}, status=404)
        return JsonResponse(to_dict(u, ['id', 'name', 'created_at']))

    def put(self, request, user_id):
        try:
            u = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "Не найден"}, status=404)
        form = UserForm(parse_body(request), instance=u)
        if not form.is_valid():
            return JsonResponse({"errors": form.errors}, status=400)
        form.save()
        return JsonResponse(to_dict(u, ['id', 'name', 'created_at']))

    def delete(self, request, user_id):
        try:
            u = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "Не найден"}, status=404)
        u.delete()
        return JsonResponse({"status": "удалён"})


@method_decorator(require_http_methods(["GET", "POST"]), name='dispatch')
class MuscleGroupListView(View):
    def get(self, request):
        groups = MuscleGroup.objects.all()
        return JsonResponse([to_dict(m, ['id', 'name', 'body_part']) for m in groups], safe=False)

    def post(self, request):
        form = MuscleGroupForm(parse_body(request))
        if not form.is_valid():
            return JsonResponse({"errors": form.errors}, status=400)
        m = form.save()
        return JsonResponse(to_dict(m, ['id', 'name', 'body_part']), status=201)


@method_decorator(require_http_methods(["GET", "PUT", "DELETE"]), name='dispatch')
class MuscleGroupDetailView(View):
    def get(self, request, group_id):
        try:
            m = MuscleGroup.objects.get(id=group_id)
        except MuscleGroup.DoesNotExist:
            return JsonResponse({"error": "Не найден"}, status=404)
        return JsonResponse(to_dict(m, ['id', 'name', 'body_part']))

    def put(self, request, group_id):
        try:
            m = MuscleGroup.objects.get(id=group_id)
        except MuscleGroup.DoesNotExist:
            return JsonResponse({"error": "Не найден"}, status=404)
        form = MuscleGroupForm(parse_body(request), instance=m)
        if not form.is_valid():
            return JsonResponse({"errors": form.errors}, status=400)
        form.save()
        return JsonResponse(to_dict(m, ['id', 'name', 'body_part']))

    def delete(self, request, group_id):
        try:
            m = MuscleGroup.objects.get(id=group_id)
        except MuscleGroup.DoesNotExist:
            return JsonResponse({"error": "Не найден"}, status=404)
        m.delete()
        return JsonResponse({"status": "удалён"})


@method_decorator(require_http_methods(["GET", "POST"]), name='dispatch')
class WorkoutListView(View):
    def get(self, request):
        workouts = Workout.objects.all()
        return JsonResponse([to_dict(w, ['id', 'user_id', 'muscle_groups_id', 'date']) for w in workouts], safe=False)

    def post(self, request):
        form = WorkoutForm(parse_body(request))
        if not form.is_valid():
            return JsonResponse({"errors": form.errors}, status=400)
        w = form.save()
        return JsonResponse(to_dict(w, ['id', 'user_id', 'muscle_groups_id', 'date']), status=201)


@method_decorator(require_http_methods(["GET", "PUT", "DELETE"]), name='dispatch')
class WorkoutDetailView(View):
    def get(self, request, workout_id):
        try:
            w = Workout.objects.get(id=workout_id)
        except Workout.DoesNotExist:
            return JsonResponse({"error": "Не найден"}, status=404)
        return JsonResponse(to_dict(w, ['id', 'user_id', 'muscle_groups_id', 'date']))

    def put(self, request, workout_id):
        try:
            w = Workout.objects.get(id=workout_id)
        except Workout.DoesNotExist:
            return JsonResponse({"error": "Не найден"}, status=404)
        form = WorkoutForm(parse_body(request), instance=w)
        if not form.is_valid():
            return JsonResponse({"errors": form.errors}, status=400)
        form.save()
        return JsonResponse(to_dict(w, ['id', 'user_id', 'muscle_groups_id', 'date']))

    def delete(self, request, workout_id):
        try:
            w = Workout.objects.get(id=workout_id)
        except Workout.DoesNotExist:
            return JsonResponse({"error": "Не найден"}, status=404)
        w.delete()
        return JsonResponse({"status": "удалён"})


@method_decorator(require_http_methods(["GET"]), name='dispatch')
class WorkoutByDateView(View):
    def get(self, request, date):
        workouts = Workout.objects.filter(date__date=date)
        return JsonResponse([to_dict(w, ['id', 'user_id', 'muscle_groups_id', 'date']) for w in workouts], safe=False)


@method_decorator(require_http_methods(["GET"]), name='dispatch')
class WorkoutByUserView(View):
    def get(self, request, user_id):
        workouts = Workout.objects.filter(user_id=user_id)
        return JsonResponse([to_dict(w, ['id', 'user_id', 'muscle_groups_id', 'date']) for w in workouts], safe=False)


@method_decorator(require_http_methods(["GET"]), name='dispatch')
class WorkoutByMuscleView(View):
    def get(self, request, group_id):
        workouts = Workout.objects.filter(muscle_groups_id=group_id)
        return JsonResponse([to_dict(w, ['id', 'user_id', 'muscle_groups_id', 'date']) for w in workouts], safe=False)


@method_decorator(require_http_methods(["GET"]), name='dispatch')
class StatsTotalView(View):
    def get(self, request, user_id):
        cnt = Workout.objects.filter(user_id=user_id).count()
        return JsonResponse({"user_id": user_id, "total_workouts": cnt})


@method_decorator(require_http_methods(["GET"]), name='dispatch')
class StatsByUserView(View):
    def get(self, request, user_id):
        stats = WorkoutStats.objects.filter(user_id=user_id)
        return JsonResponse([to_dict(s, ['id', 'user_id', 'muscle_group', 'last_date', 'total']) for s in stats], safe=False)


@method_decorator(require_http_methods(["GET"]), name='dispatch')
class StatsRegularityView(View):
    def get(self, request):
        result = {}
        for s in WorkoutStats.objects.all():
            total = s.total or 0
            result[s.muscle_group] = {
                "total": total,
                "last_date": str(s.last_date) if s.last_date else None,
                "avg_days": round(30 / total, 1) if total > 0 else 0
            }
        return JsonResponse(result)


@method_decorator(require_http_methods(["POST"]), name='dispatch')
class StatsUpdateView(View):
    def post(self, request):
        WorkoutStats.objects.all().delete()
        for w in Workout.objects.all():
            name = w.muscle_groups.name
            stat, _ = WorkoutStats.objects.get_or_create(
                user=w.user,
                muscle_group=name,
                defaults={'last_date': w.date, 'total': 0}
            )
            stat.total += 1
            if not stat.last_date or w.date > stat.last_date:
                stat.last_date = w.date
            stat.save()
        return JsonResponse({"status": "обновлено"})