import math


class DistanceTravelledManager(object):

    def __init__(self, distances):
        self.distances = distances

    # Calcula la varianza actual de los km de viaje de todos los equipos
    def calculate_km_traveled_variance(self, fixture):
        km_traveled_variance = 0
        km_traveled_per_team = self.__calculate_km_traveled_per_team__(fixture)
        media = self.__calculate_km_traveled_media__(km_traveled_per_team)

        for distance in km_traveled_per_team.values():
            km_traveled_variance += (distance - media)**2
        km_traveled_variance/len(km_traveled_per_team)

        return round(math.sqrt(km_traveled_variance), 2)

    # Calcula los km recorridos por cada equipo
    def __calculate_km_traveled_per_team__(self, fixture):
        '''
        Formato de los km recorridos por equipo:
            {"Equipo A": 100,
            ...,
            "Equipo Z": 200
            }
        '''
        km_traveled_per_team = {}
        for matches in fixture:
            for match in matches:
                local_team, away_team = match[0], match[1]

                if away_team not in km_traveled_per_team:
                    km_traveled_per_team[away_team] = 0
                km_traveled_per_team[away_team] +=\
                    int(self.distances[away_team][local_team])

        return km_traveled_per_team

    # Calcula la media de los km recorridos por los equipos
    def __calculate_km_traveled_media__(self, km_traveled_per_team):
        return sum(km_traveled_per_team.values())/len(km_traveled_per_team)
