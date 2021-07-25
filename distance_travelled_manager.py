import math


class DistanceTravelledManager(object):

    def __init__(self, distances):
        self.distances = distances

    # Calcula la varianza actual de los km de viaje de todos los equipos
    def calculate_km_travelled_variance(self, fixture):
        km_travelled_variance = 0
        km_travelled_per_team = self.\
            calculate_km_travelled_per_team(fixture)
        media = self.__calculate_km_travelled_media__(km_travelled_per_team)

        for distance in km_travelled_per_team.values():
            km_travelled_variance += (distance - media)**2
        km_travelled_variance/len(km_travelled_per_team)

        return round(math.sqrt(km_travelled_variance), 2)

    # Calcula los km recorridos por cada equipo
    def calculate_km_travelled_per_team(self, fixture):
        '''
        Formato de los km recorridos por equipo:
            {"Equipo A": 100,
            ...,
            "Equipo Z": 200
            }
        '''
        km_travelled_per_team = {}
        for matches in fixture:
            for match in matches:
                local_team, away_team = match[0], match[1]

                if away_team not in km_travelled_per_team:
                    km_travelled_per_team[away_team] = 0
                km_travelled_per_team[away_team] +=\
                    int(self.distances[away_team][local_team])

        return km_travelled_per_team

    # Calcula la media de los km recorridos por los equipos
    def __calculate_km_travelled_media__(self, km_travelled_per_team):
        return sum(km_travelled_per_team.values())/len(km_travelled_per_team)
