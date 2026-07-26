from worlds.LauncherComponents import Component, Type, components, launch

def run_client(*args: str) -> None:
    from .client.launch import launch_tf04_client
    
    launch(launch_tf04_client, name="Transformers (2004) Client", args=args)
    
    
    
components.append(
    Component(
        "Transformers (2004) Client",
        func=run_client,
        game_name="Transformers (2004)",
        component_type=Type.CLIENT,
        supports_uri=True,
    )
)