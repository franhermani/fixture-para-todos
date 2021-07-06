class FixtureManager(object):
    '''
    Formato del fixture (cada elemento de la lista es una fecha):
        [
            [("Equipo A", "Equipo B"),
            (..., ...),
            ("Equipo Y", "Equipo Z")],
            ...,
            [("Equipo A", "Equipo B"),
            (..., ...),
            ("Equipo Y", "Equipo Z")]
        ]
    '''
    def __init__(self, teams, distances):
        self.teams = teams
        self.distances = distances

    # Calcula el fixture del torneo minimizando la varianza
    # de los km de viaje de todos los equipos
    def calculate_initial_fixture(self):
        fixture = [
            [("Boca Juniors", "River Plate"), ("Belgrano", "Talleres")],
            [("Talleres", "Boca Juniors"), ("River Plate", "Belgrano")],
            [("Boca Juniors", "Belgrano"), ("Talleres", "River Plate")]
        ]

        # TODO: cada vez que calculo el fixture, chequear las restricciones.
        # Si no se cumple alguna, tendria que encontrar una forma piola de
        # realizar intercambios hasta que se cumpla o de generar
        # un nuevo fixture de cero que sí cumpla

        return fixture

    # Imprime el fixture por pantalla
    def print(self, fixture):
        print("--------------------------------------------------------------")
        print("--------------------- FIXTURE PARA TODOS ---------------------")
        print("--------------------------------------------------------------")

        i = 1
        for matchday in fixture:
            print("\nFecha " + str(i) + ":")
            i += 1

            for match in matchday:
                local_team, away_team = match[0], match[1]
                print("\t" + local_team + "\t\tVs.\t\t" + away_team)
