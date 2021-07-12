import math


class DistanceTravelledManager(object):

    def __init__(self, distances):
        self.distances = distances

    # Calcula la varianza actual de los km de viaje de todos los equipos
    def calculate_km_travelled_variance(self, fixture):
        km_travelled_variance = 0
        km_travelled_per_team = self.\
            __calculate_km_travelled_per_team__(fixture)
        media = self.__calculate_km_travelled_media__(km_travelled_per_team)

        print("Km recorridos por cada equipo:")
        for team, km in km_travelled_per_team.items():
            print("- " + team + ": " + str(km))

        for distance in km_travelled_per_team.values():
            km_travelled_variance += (distance - media)**2
        km_travelled_variance/len(km_travelled_per_team)

        print("\nVarianza de los km recorridos por todos los equipos:")
        return round(math.sqrt(km_travelled_variance), 2)

    # Calcula los km recorridos por cada equipo
    def __calculate_km_travelled_per_team__(self, fixture):
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

    # Devuelve una lista con la dispersion de los equipos
    def __calculate_teams_dispersion__(self, fixture):
        km_travelled_per_team = self.\
            __calculate_km_travelled_per_team__(fixture)
        media = self.__calculate_km_travelled_media__(km_travelled_per_team)

        teams_dispersion = {}
        for team, km in km_travelled_per_team.items():
            teams_dispersion[team] = abs(km - media)

        teams_dispersion_ordered = dict(sorted(teams_dispersion.items(),
                                        key=lambda item: item[1])[::-1])

        return list(teams_dispersion_ordered.keys())
