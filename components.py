from worlds.LauncherComponents import Component, Type, components, launch_subprocess
from ..LauncherComponents import icon_paths




def run_client(*args: str) -> None:
    from .client.launch import launch_tf04_client
    
    launch_subprocess(launch_tf04_client, name="Transformers (2004) Client", args=args)
    
    
    
components.append(
    Component(
        "Transformers (2004) Client",
        icon="tf04_icon",
        func=run_client,
        game_name="Transformers (2004)",
        component_type=Type.CLIENT,
        supports_uri=True,
    )
)

icon_paths["tf04_icon"] = f"ap:{__name__}/assets/tf04_icon.png"