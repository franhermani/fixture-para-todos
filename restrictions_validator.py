
class RestrictionsValidator(object):

    def __init__(self):
        self.param_r1 = 1
        self.param_r2 = 1
        self.param_r3 = 2

    def validate_fixture(self, fixture, derbies, teams):
        return self.validate_r1_and_r2(fixture, teams) and\
               self.validate_r3(fixture, teams) and\
               self.validate_r4(fixture, derbies, teams)

    def validate_r1_and_r2(self, fixture, teams):
        '''
        - R1: Todos los equipos deben jugar la misma cantidad de partidos de
          local y de visitante que el resto o, a lo sumo,<param_r1> partido/s
          de diferencia con respecto al resto de los equipos
        - R2: Todos los equipos deben jugar la misma cantidad de partidos
          de local y de visitante o, a lo sumo, <param_r2> partido/s
          de diferencia entre ambas condiciones
        '''
        local_matches_per_team = {i: 0 for i in teams}
        away_matches_per_team = {i: 0 for i in teams}

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
        for team in teams:
            local_matches = local_matches_per_team[team]\
                if team in local_matches_per_team else 0
            away_matches = away_matches_per_team[team]\
                if team in away_matches_per_team else 0
            if abs(local_matches - away_matches) > self.param_r2:
                return False

        return True

    def validate_r3(self, fixture, teams):
        '''
        R3: Ningún equipo puede jugar más de <param_r3> partidos
        consecutivos en la misma condición
        '''
        last_condition_per_team = {i: "X" for i in teams}
        consecutive_per_team = {i: 1 for i in teams}

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

    def validate_r4(self, fixture, derbies, teams):
        '''
        R4: Los equipos considerados clásicos entre sí no pueden jugar
        en la misma condición en la misma fecha.
        '''
        for matchday in fixture:
            for match in matchday:
                local_team, away_team = match[0], match[1]
                # TODO: ...

        return True
