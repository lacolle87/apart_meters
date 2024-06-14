def format_metrics(metrics):
    if not metrics:
        return "You have not recorded any water metrics yet."
    return "Your metrics:\n" + "\n".join([f"{electric_usage} {water_usage}" for electric_usage, water_usage in metrics])
