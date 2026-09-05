"""Relatório textual da navegação e do conhecimento v0.1."""

from datetime import date

from quintoimperio.domain import KnowledgeModel, NavigationModel, monsoon_phase


if __name__ == "__main__":
    navigation = NavigationModel()
    knowledge = KnowledgeModel()

    distance = navigation.route_geodesic_nm("R_MAL_CAL")
    april = navigation.estimate_duration_days("R_MAL_CAL", date(1498, 4, 24), seed=1498)
    june = navigation.estimate_duration_days("R_MAL_CAL", date(1498, 6, 24), seed=1498)

    print("Quinto Império — navegação v0.1")
    print("Distâncias e durações abaixo são índices/calibrações do protótipo, não medidas da rota histórica efetivamente navegada.")
    print(f"R_MAL_CAL distância geodésica: {distance:.1f} nm")
    print(f"Observações históricas preservadas: {navigation.observed_days('R_MAL_CAL')} dias")
    print(f"Progresso diário de referência: {navigation.reference_daily_nm:.1f} nm/dia")
    print(f"Estimativa partida 1498-04-24: {april:.1f} dias ({monsoon_phase(date(1498, 4, 24)).value})")
    print(f"Estimativa partida 1498-06-24: {june:.1f} dias ({monsoon_phase(date(1498, 6, 24)).value})")
    print(f"SOF->KIL distância: {navigation.route_geodesic_nm('R_SOF_KIL')}")
    print("Conhecimento inicial CAL/PLAYER:", knowledge.initial_for_node("CAL", "PLAYER"))
    print("Conhecimento inicial CAL/CROWN:", knowledge.initial_for_node("CAL", "CROWN"))
