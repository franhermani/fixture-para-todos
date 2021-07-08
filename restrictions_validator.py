class RestrictionsValidator(object):

    def __init__(self, teams, derbies, restrictions_params):
        self.teams = teams
        self.derbies = derbies
        self.param_r1 = restrictions_params["r1"]
        self.param_r2 = restrictions_params["r2"]
        self.param_r3 = restrictions_params["r3"]

    def validate_fixture(self, fixture):
        return self.__validate_r1_and_r2__(fixture) and\
               self.__validate_r3__(fixture) and\
               self.__validate_r4__(fixture)

    def __validate_r1_and_r2__(self, fixture):
        '''
        - R1: Todos los equipos deben jugar la misma cantidad de partidos de
          local y de visitante que el resto o, a lo sumo, <param_r1> partido/s
          de diferencia con respecto al resto de los equipos
        - R2: Todos los equipos deben jugar la misma cantidad de partidos
          de local y de visitante o, a lo sumo, <param_r2> partido/s
          de diferencia entre ambas condiciones
        '''
        local_matches_per_team = {i: 0 for i in self.teams}
        away_matches_per_team = {i: 0 for i in self.teams}

        for matches in fixture:
            for match in matches:
                local_team, away_team = match[0], match[1]
                local_matches_per_team[local_team] += 1
                away_matches_per_team[away_team] += 1

        # (R1) Compruebo partidos de local
        local_matches = set(local_matches_per_team.values())
        for x in local_matches:
            for y in local_matches:
                if abs(x - y) > self.param_r1:
                    return False

        # (R1) Compruebo partidos de visitante
        away_matches = set(away_matches_per_team.values())
        for x in away_matches:
            for y in away_matches:
                if abs(x - y) > self.param_r1:
                    return False

        # (R2) Compruebo partidos de local y de visitante de cada equipo
        for team in self.teams:
            local_matches = local_matches_per_team[team]\
                if team in local_matches_per_team else 0
            away_matches = away_matches_per_team[team]\
                if team in away_matches_per_team else 0
            if abs(local_matches - away_matches) > self.param_r2:
                return False

        return True

    def __validate_r3__(self, fixture):
        '''
        R3: Ningún equipo puede jugar más de <param_r3> partidos
        consecutivos en la misma condición
        '''
        last_condition_per_team = {i: "X" for i in self.teams}
        consecutive_per_team = {i: 1 for i in self.teams}

        for matchday in fixture:
            for match in matchday:
                local_team, away_team = match[0], match[1]

                if last_condition_per_team[local_team] == "Local":
                    consecutive_per_team[local_team] += 1
                    if consecutive_per_team[local_team] > self.param_r3:
                        return False
                else:
                    consecutive_per_team[local_team] = 1

                if last_condition_per_team[away_team] == "Away":
                    consecutive_per_team[away_team] += 1
                    if consecutive_per_team[away_team] > self.param_r3:
                        return False
                else:
                    consecutive_per_team[away_team] = 1

                last_condition_per_team[local_team] = "Local"
                last_condition_per_team[away_team] = "Away"

        return True

    def __validate_r4__(self, fixture):
        '''
        R4: Los equipos considerados clásicos entre sí no pueden jugar
        de local en la misma fecha.
        '''
        condition_per_team = {i: "X" for i in self.teams}

        for matchday in fixture:
            for match in matchday:
                local_team, away_team = match[0], match[1]
                condition_per_team[local_team] = "Local"
                condition_per_team[away_team] = "Away"

            for team1, team2 in self.derbies.items():
                if condition_per_team[team1] == condition_per_team[team2] and\
                   condition_per_team[team1] == "Local":
                    return False

        return True
