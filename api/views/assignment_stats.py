from math import floor

from django.db.models import Max, F, Count
from rest_framework import generics
from rest_framework.response import Response

from api.models import Run
from canvas.models import AvatarConfig


class AssignmentStatsView(generics.RetrieveAPIView):

    # HTTP METHODS
    def get(self, request, *args, **kwargs):
        assignment_id = kwargs['id']
        data = {}

        # LEADERBOARD
        # TODO: when saving the score from an assigment set the highest score from all the runs so this query isn't so hard :(
        # TODO: sort the result of leaderboard_runs
        leaderboard_runs = Run.objects.all().filter(assignment=assignment_id).values('user', 'user__name').annotate(Max('score'))
        sorted_runs = [r for r in leaderboard_runs]
        sorted_runs.sort(key= lambda r : r['score__max'], reverse=True)
        configs = AvatarConfig.objects.filter(user__in=[x['user'] for x in leaderboard_runs])

        for config in configs:
            for leaderboard_run in sorted_runs:
                if leaderboard_run['user'] == config.user_id:
                    leaderboard_run['avatar_config'] = config.config

        data['leaderboard'] = {
            'data': sorted_runs,
        }
        [print(x) for x in sorted_runs]

        SCORE_RESOLUTION = 10
        # SCORE HISTOGRAM
        score_histogram = {key * SCORE_RESOLUTION: 0 for key in range(int(100 / SCORE_RESOLUTION)+1)}
        for r in leaderboard_runs:
            score_histogram[floor(r['score__max'] / SCORE_RESOLUTION) * SCORE_RESOLUTION] += 1
        data['score_histogram'] = {
            'data': score_histogram,
            'raw': [r['score__max'] for r in leaderboard_runs],
            'x_min': 0,
            'x_max': 100,
            'y_min': 0,
            'y_max': 100,
            # 'avg': sum([r['score__max'] for r in leaderboard_runs]) / len(leaderboard_runs),
            # 'mean': leaderboard_runs[len(leaderboard_runs) // 2]['score__max'],
            'resolution': SCORE_RESOLUTION,
        }

        # TIME HISTOGRAM
        # TODO: sort the result of timed_runs
        TIME_RESOLUTION = 10
        timed_runs = Run.objects.all().filter(assignment=assignment_id).values('id').annotate(time=F('end_date') - F('start_date')).annotate(Max('score'))
        time_histogram = {}
        for r in timed_runs:
            bin_number = floor(r['time'].seconds / 60 / TIME_RESOLUTION) * TIME_RESOLUTION
            if (bin_number in time_histogram.keys()):
                time_histogram[bin_number] += 1
            else:
                time_histogram[bin_number] = 1
        data['time_histogram'] = {
            'data': time_histogram,
            'raw': [r['time'].seconds / 60 for r in timed_runs],
            'x_min': min([int(k) for k in time_histogram.keys()] + [0]),
            'x_max': max([int(k) for k in time_histogram.keys()] + [0]),
            'y_min': 0,
            'y_max': max([int(k) for k in time_histogram.values()] + [0]),
            # 'avg': sum([r['time'].seconds for r in timed_runs]) / len(timed_runs) / 60,
            # 'mean': timed_runs[len(timed_runs) // 2]['time'].seconds / 60,
            'resolution': TIME_RESOLUTION,
        }

        # TRIES HISTOGRAM
        # TODO: sort the result of timed_runs
        tries_runs = Run.objects.all().filter(assignment=assignment_id).values('user').annotate(Count('user'))
        tries_histogram = {}
        for r in tries_runs:
            count = r['user__count']
            if (count in tries_histogram.keys()):
                tries_histogram[count] += 1
            else:
                tries_histogram[count] = 1
        data['tries_histogram'] = {
            'data': tries_histogram,
            'raw': [r['user__count'] for r in tries_runs],
            'x_min': 0,
            'x_max': max([int(k) for k in tries_histogram.keys()] + [0]),
            'y_min': 0,
            'y_max': max([int(k) for k in tries_histogram.values()] + [0]),
            # 'avg': sum([r['user__count'] for r in tries_runs]) / len(tries_runs),
            # 'mean': tries_runs[len(tries_runs) // 2]['user__count'],
            'resolution': 10,
        }

        return Response(data)
    
    """
    return data shape
    {
        leaderboard: {
            data: {index: value},
            scale_min: value
            scale_max: value
            avg: value
            mean: value
        },

    }
    """
