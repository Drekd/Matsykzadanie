import json
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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


@csrf_exempt
def users_all(request):
    if request.method == 'GET':
        return JsonResponse(
            [to_dict(u, ['id', 'name', 'created_at']) for u in User.objects.all()],
            safe=False
        )
    if request.method == 'POST':
        data = parse_body(request)
        if not data.get('name'):
            return JsonResponse({"error": "name обязателен"}, status=400)
        u = User.objects.create(name=data['name'])
        return JsonResponse(to_dict(u, ['id', 'name', 'created_at']), status=201)


@csrf_exempt
def user_detail(request, user_id):
    try:
        u = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "Не найден"}, status=404)

    if request.method == 'GET':
        return JsonResponse(to_dict(u, ['id', 'name', 'created_at']))

    if request.method == 'PUT':
        data = parse_body(request)
        if data.get('name'):
            u.name = data['name']
            u.save()
        return JsonResponse(to_dict(u, ['id', 'name', 'created_at']))

    if request.method == 'DELETE':
        u.delete()
        return JsonResponse({"status": "удалён"})


@csrf_exempt
def muscle_groups_all(request):
    if request.method == 'GET':
        return JsonResponse(
            [to_dict(m, ['id', 'name', 'body_part']) for m in MuscleGroup.objects.all()],
            safe=False
        )
    if request.method == 'POST':
        data = parse_body(request)
        if not data.get('name') or not data.get('body_part'):
            return JsonResponse({"error": "name и body_part обязательны"}, status=400)
        m = MuscleGroup.objects.create(name=data['name'], body_part=data['body_part'])
        return JsonResponse(to_dict(m, ['id', 'name', 'body_part']), status=201)


@csrf_exempt
def muscle_group_detail(request, group_id):
    try:
        m = MuscleGroup.objects.get(id=group_id)
    except MuscleGroup.DoesNotExist:
        return JsonResponse({"error": "Не найден"}, status=404)

    if request.method == 'GET':
        return JsonResponse(to_dict(m, ['id', 'name', 'body_part']))

    if request.method == 'PUT':
        data = parse_body(request)
        if data.get('name'):
            m.name = data['name']
        if data.get('body_part'):
            m.body_part = data['body_part']
        m.save()
        return JsonResponse(to_dict(m, ['id', 'name', 'body_part']))

    if request.method == 'DELETE':
        m.delete()
        return JsonResponse({"status": "удалён"})


@csrf_exempt
def workouts_all(request):
    if request.method == 'GET':
        data = [
            to_dict(w, ['id', 'user_id', 'muscle_groups_id', 'date'])
            for w in Workout.objects.all()
        ]
        return JsonResponse(data, safe=False)

    if request.method == 'POST':
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


@csrf_exempt
def workout_detail(request, workout_id):
    try:
        w = Workout.objects.get(id=workout_id)
    except Workout.DoesNotExist:
        return JsonResponse({"error": "Не найден"}, status=404)

    if request.method == 'GET':
        return JsonResponse(to_dict(w, ['id', 'user_id', 'muscle_groups_id', 'date']))

    if request.method == 'PUT':
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

    if request.method == 'DELETE':
        w.delete()
        return JsonResponse({"status": "удалён"})


def workouts_by_date(request, date):
    workouts = Workout.objects.filter(date__date=date)
    return JsonResponse(
        [to_dict(w, ['id', 'user_id', 'muscle_groups_id', 'date']) for w in workouts],
        safe=False
    )


def workouts_by_user(request, user_id):
    workouts = Workout.objects.filter(user_id=user_id)
    return JsonResponse(
        [to_dict(w, ['id', 'user_id', 'muscle_groups_id', 'date']) for w in workouts],
        safe=False
    )


def workouts_by_muscle(request, group_id):
    workouts = Workout.objects.filter(muscle_groups_id=group_id)
    return JsonResponse(
        [to_dict(w, ['id', 'user_id', 'muscle_groups_id', 'date']) for w in workouts],
        safe=False
    )


def stats_total(request, user_id):
    cnt = Workout.objects.filter(user_id=user_id).count()
    return JsonResponse({"user_id": user_id, "total_workouts": cnt})


def stats_by_user(request, user_id):
    stats = WorkoutStats.objects.filter(user_id=user_id)
    return JsonResponse(
        [to_dict(s, ['id', 'user_id', 'muscle_group', 'last_date', 'total']) for s in stats],
        safe=False
    )


def stats_regularity(request):
    result = {}
    for s in WorkoutStats.objects.all():
        total = s.total or 0
        result[s.muscle_group] = {
            "total": total,
            "last_date": str(s.last_date) if s.last_date else None,
            "avg_days": round(30 / total, 1) if total > 0 else 0
        }
    return JsonResponse(result)


@csrf_exempt
def stats_update(request):
    """Пересчёт статистики по всем тренировкам"""
    if request.method != 'POST':
        return JsonResponse({"error": "только POST"}, status=405)

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