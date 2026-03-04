from dataset_builder.export_parquet import salvar_parquet

dados = [
    {
        "timestamp": "2026-03-01T12:30:00",
        "hour": 12,
        "weekday": 6,
        "event_type": "arquivo_detectado",
        "extension": "mp3",
        "filename_length": 18,
        "folder": "Desktop"
    }
]

salvar_parquet(dados)
