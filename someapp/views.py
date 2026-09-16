import json
from datetime import datetime
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import User, MuscleGroup, Workout, WorkoutStats


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



@method_decorator(csrf_exempt, name='dispatch')
class UserListView(View):
    """GET /users/  |  POST /users/"""

    def get(self, request):
        users = User.objects.all()
        return JsonResponse(
            [to_dict(u, ['id', 'name', 'created_at']) for u in users],
            safe=False
        )

    def post(self, request):
        data = parse_body(request)
        if not data.get('name'):
            return JsonResponse({"error": "name обязателен"}, status=400)
        u = User.objects.create(name=data['name'])
        return JsonResponse(to_dict(u, ['id', 'name', 'created_at']), status=201)


@method_decorator(csrf_exempt, name='dispatch')
class UserDetailView(View):
    """GET /users/{id}/  |  PUT /users/{id}/  |  DELETE /users/{id}/"""

    def get_object(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    def get(self, request, user_id):
        u = self.get_object(user_id)
        if not u:
            return JsonResponse({"error": "Не найден"}, status=404)
        return JsonResponse(to_dict(u, ['id', 'name', 'created_at']))

    def put(self, request, user_id):
        u = self.get_object(user_id)
        if not u:
            return JsonResponse({"error": "Не найден"}, status=404)
        data = parse_body(request)
        if data.get('name'):
            u.name = data['name']
            u.save()
        return JsonResponse(to_dict(u, ['id', 'name', 'created_at']))

    def delete(self, request, user_id):
        u = self.get_object(user_id)
        if not u:
            return JsonResponse({"error": "Не найден"}, status=404)
        u.delete()
        return JsonResponse({"status": "удалён"})


@method_decorator(csrf_exempt, name='dispatch')
class MuscleGroupListView(View):
    """GET /muscle_groups/  |  POST /muscle_groups/"""

    def get(self, request):
        groups = MuscleGroup.objects.all()
        return JsonResponse(
            [to_dict(m, ['id', 'name', 'body_part']) for m in groups],
            safe=False
        )

    def post(self, request):
        data = parse_body(request)
        if not data.get('name') or not data.get('body_part'):
            return JsonResponse({"error": "name и body_part обязательны"}, status=400)
        m = MuscleGroup.objects.create(name=data['name'], body_part=data['body_part'])
        return JsonResponse(to_dict(m, ['id', 'name', 'body_part']), status=201)


@method_decorator(csrf_exempt, name='dispatch')
class MuscleGroupDetailView(View):
    """GET | PUT | DELETE /muscle_groups/{id}/"""

    def get_object(self, group_id):
        try:
            return MuscleGroup.objects.get(id=group_id)
        except MuscleGroup.DoesNotExist:
            return None

    def get(self, request, group_id):
        m = self.get_object(group_id)
        if not m:
            return JsonResponse({"error": "Не найден"}, status=404)
        return JsonResponse(to_dict(m, ['id', 'name', 'body_part']))

    def put(self, request, group_id):
        m = self.get_object(group_id)
        if not m:
            return JsonResponse({"error": "Не найден"}, status=404)
        data = parse_body(request)
        if data.get('name'):
            m.name = data['name']
        if data.get('body_part'):
            m.body_part = data['body_part']
        m.save()
        return JsonResponse(to_dict(m, ['id', 'name', 'body_part']))

    def delete(self, request, group_id):
        m = self.get_object(group_id)
        if not m:
            return JsonResponse({"error": "Не найден"}, status=404)
        m.delete()
        return JsonResponse({"status": "удалён"})



@method_decorator(csrf_exempt, name='dispatch')
class WorkoutListView(View):
    """GET /workouts/  |  POST /workouts/"""

    def get(self, request):
        workouts = Workout.objects.all()
        return JsonResponse(
            [to_dict(w, ['id', 'user_id', 'muscle_groups_id', 'date']) for w in workouts],
            safe=False
        )

    def post(self, request):
        data = parse_body(request)
        try:
            user = User.objects.get(id=data['user_id'])
            group = MuscleGroup.objects.get(id=data['muscle_groups_id'])
        except (KeyError, User.DoesNotExist, MuscleGroup.DoesNotExist):
            return JsonResponse({"error": "user_id или muscle_groups_id неверны"}, status=400)

        w = Workout.objects.create(
            user=user,
            muscle_groups=group,
            date=data.get('date', datetime.now())
        )
        return JsonResponse(
            to_dict(w, ['id', 'user_id', 'muscle_groups_id', 'date']),
            status=201
        )


@method_decorator(csrf_exempt, name='dispatch')
class WorkoutDetailView(View):
    """GET | PUT | DELETE /workouts/{id}/"""

    def get_object(self, workout_id):
        try:
            return Workout.objects.get(id=workout_id)
        except Workout.DoesNotExist:
            return None

    def get(self, request, workout_id):
        w = self.get_object(workout_id)
        if not w:
            return JsonResponse({"error": "Не найден"}, status=404)
        return JsonResponse(to_dict(w, ['id', 'user_id', 'muscle_groups_id', 'date']))

    def put(self, request, workout_id):
        w = self.get_object(workout_id)
        if not w:
            return JsonResponse({"error": "Не найден"}, status=404)
        data = parse_body(request)
        if data.get('muscle_groups_id'):
            try:
                w.muscle_groups = MuscleGroup.objects.get(id=data['muscle_groups_id'])
            except MuscleGroup.DoesNotExist:
                return JsonResponse({"error": "Группа не найдена"}, status=400)
        if data.get('date'):
            w.date = data['date']
        w.save()
        return JsonResponse(to_dict(w, ['id', 'user_id', 'muscle_groups_id', 'date']))

    def delete(self, request, workout_id):
        w = self.get_object(workout_id)
        if not w:
            return JsonResponse({"error": "Не найден"}, status=404)
        w.delete()
        return JsonResponse({"status": "удалён"})


class WorkoutByDateView(View):
    """GET /workouts/date/{date}/"""

    def get(self, request, date):
        workouts = Workout.objects.filter(date__date=date)
        return JsonResponse(
            [to_dict(w, ['id', 'user_id', 'muscle_groups_id', 'date']) for w in workouts],
            safe=False
        )


class WorkoutByUserView(View):
    """GET /workouts/user/{user_id}/"""

    def get(self, request, user_id):
        workouts = Workout.objects.filter(user_id=user_id)
        return JsonResponse(
            [to_dict(w, ['id', 'user_id', 'muscle_groups_id', 'date']) for w in workouts],
            safe=False
        )


class WorkoutByMuscleView(View):
    """GET /workouts/muscle/{group_id}/"""

    def get(self, request, group_id):
        workouts = Workout.objects.filter(muscle_groups_id=group_id)
        return JsonResponse(
            [to_dict(w, ['id', 'user_id', 'muscle_groups_id', 'date']) for w in workouts],
            safe=False
        )


class StatsTotalView(View):
    """GET /stats/total/{user_id}/"""

    def get(self, request, user_id):
        cnt = Workout.objects.filter(user_id=user_id).count()
        return JsonResponse({"user_id": user_id, "total_workouts": cnt})


class StatsByUserView(View):
    """GET /stats/user/{user_id}/"""

    def get(self, request, user_id):
        stats = WorkoutStats.objects.filter(user_id=user_id)
        return JsonResponse(
            [to_dict(s, ['id', 'user_id', 'muscle_group', 'last_date', 'total']) for s in stats],
            safe=False
        )


class StatsRegularityView(View):
    """GET /stats/regularity/"""

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


@method_decorator(csrf_exempt, name='dispatch')
class StatsUpdateView(View):
    """POST /stats/update/"""

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