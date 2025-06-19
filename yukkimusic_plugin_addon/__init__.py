handlers = []

def register(event_type: str, *args, **kwargs):
    def decorator(func):
        handlers.append({
            "event": event_type,
            "args": args,
            "kwargs": kwargs,
            "func": func
        })
        return func
    return decorator

async def setup(ctx: "LoaderContext"):
    for handler in handlers:
        if handler["event"] == "message":
            ctx.app.on_message(*handler["args"], **handler["kwargs"])(handler["func"])
        elif handler["event"] == "callback_query":
            ctx.app.on_callback_query(*handler["args"], **handler["kwargs"])(handler["func"])