# fluxpoint.py
fluxpoint.py is a library for interacting with the fluxpoint API\
Using this rich library allows us to grab a variety of SFW, NSFW images and gifs, and even generate our own images!

## Docs
https://fluxpointdev.github.io/fluxpoint-py

```python
import asyncio;
from fluxpoint import FluxpointClient;

fluxpointclient = Fluxpointclient("token");

async def main():
    # Get a simple SFW neko image.
    res = await fluxpointclient.sfw.getNekoImage();

    # Good practice to make sure your response was successful!
    if res.success: 
        print(res.file); # Prints link to SFW neko image.

    # Get a simple NSFW neko image.
    res = await fluxpointclent.nsfw.getNekoImage();

    if res.success:
        print(res.file); # Prints link to NSFW neko image.
    
asyncio.run(main());
```
