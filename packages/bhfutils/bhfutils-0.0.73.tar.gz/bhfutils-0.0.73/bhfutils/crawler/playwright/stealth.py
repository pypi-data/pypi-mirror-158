import json
from logging import Logger
from dataclasses import dataclass
from typing import Tuple, Optional, Dict

from importlib import resources
from playwright.async_api import Page as AsyncPage
from playwright.sync_api import Page as SyncPage


def from_file(name):
    """read script from /js data directory"""
    return resources.read_text(f'{__package__}.js', name)


SCRIPTS: Dict[str, str] = {
    'chrome_app': from_file('chrome.app.js'),
    'chrome_csi': from_file('chrome.csi.js'),
    'chrome_loadtimes': from_file('chrome.loadtimes.js'),
    'chrome_runtime': from_file('chrome.runtime.js'),
    'hairline': from_file('hairline.js'),
    'iframe_content_window': from_file('iframe.contentWindow.js'),
    'magic-arrays': from_file('magic-arrays.js'),
    'media_codecs': from_file('media.codecs.js'),
    'navigator_hardware_concurrency': from_file('navigator.hardwareConcurrency.js'),
    'navigator_languages': from_file('navigator.languages.js'),
    'navigator_permissions': from_file('navigator.permissions.js'),
    'navigator_platform': from_file('navigator.platform.js'),
    'navigator_plugins': from_file('navigator.plugins.js'),
    'navigator_user_agent': from_file('navigator.userAgent.js'),
    'navigator_vendor': from_file('navigator.vendor.js'),
    'navigator_webdriver': from_file('navigator.webdriver.js'),
    'touchScreen': from_file('screen.touch.js'),
    'utils': from_file('utils.js'),
    'webgl_vendor': from_file('webgl.vendor.js'),
    'dimensions': from_file('window.dimensions.js'),
}


@dataclass
class StealthConfig:
    """
    Playwright Stealth Configuration that applies stealth strategies to Playwright Page objects.

    The stealth strategies are contained in /js package and are basic javascript scripts that are executed
    on every Page.goto call.

    Note:
        All init scripts are combined by playwright into one script and then executed this means
        the scripts should not have conflicting constants/variables etc. !
        This also means scripts can be extended by overriding enabled_scripts generator:

        ```
        @property
        def enabled_scripts():
            yield 'console.log("first script")'
            yield from super().enabled_scripts()
            yield 'console.log("last script")'
        ```
    """
    # scripts
    hairline: bool = False
    dimensions: bool = True
    screen_touch: bool = True
    media_codecs: bool = True
    iframe_content_window: bool = False
    chrome_csi: bool = False
    chrome_app: bool = False
    chrome_runtime: bool = False
    chrome_loadtimes: bool = False
    webdriver: bool = False
    webgl_vendor: bool = True
    navigator_vendor: bool = True
    navigator_plugins: bool = True
    navigator_platform: bool = True
    navigator_languages: bool = False
    navigator_user_agent: bool = False
    navigator_permissions: bool = False
    navigator_hardware_concurrency: bool = True

    # options
    max_touch_points: int = 5
    vendor: str = 'Apple Inc.'
    renderer: str = 'Apple GPU'
    nav_vendor: str = 'Apple Computer, Inc.'
    nav_platform: str = 'iPhone'
    nav_user_agent: str = None
    languages: Tuple[str] = ('en-US', 'en')
    hardware_concurrency: int = -1
    runOnInsecureOrigins: Optional[bool] = None

    @property
    def enabled_scripts(self):
        opts = json.dumps({
            'webgl_vendor': self.vendor,
            'webgl_renderer': self.renderer,
            'navigator_vendor': self.nav_vendor,
            'navigator_platform': self.nav_platform,
            'navigator_user_agent': self.nav_user_agent,
            'languages': list(self.languages),
            'max_touch_points': self.max_touch_points,
            'hardwareConcurrency': self.hardware_concurrency,
            'runOnInsecureOrigins': self.runOnInsecureOrigins,
        })
        # defined options constant
        yield f'const opts = {opts}'
        # init utils and magic-arrays helper
        yield SCRIPTS['utils']
        yield SCRIPTS['magic-arrays']

        if self.hairline:
            yield SCRIPTS['hairline']
        if self.dimensions:
            yield SCRIPTS['dimensions']
        if self.screen_touch:
            yield SCRIPTS['touchScreen']
        if self.media_codecs:
            yield SCRIPTS['media_codecs']
        if self.iframe_content_window:
            yield SCRIPTS['iframe_content_window']
        if self.chrome_csi:
            yield SCRIPTS['chrome_csi']
        if self.chrome_app:
            yield SCRIPTS['chrome_app']
        if self.chrome_runtime:
            yield SCRIPTS['chrome_runtime']
        if self.chrome_loadtimes:
            yield SCRIPTS['chrome_loadtimes']
        if self.webgl_vendor:
            yield SCRIPTS['webgl_vendor']
        if self.navigator_vendor:
            yield SCRIPTS['navigator_vendor']
        if self.navigator_platform:
            yield SCRIPTS['navigator_platform']
        if self.webdriver:
            yield SCRIPTS['navigator_webdriver']
        if self.navigator_plugins:
            yield SCRIPTS['navigator_plugins']
        if self.navigator_permissions:
            yield SCRIPTS['navigator_permissions']
        if self.navigator_languages:
            yield SCRIPTS['navigator_languages']
        if self.navigator_user_agent:
            yield SCRIPTS['navigator_user_agent']
        if self.navigator_hardware_concurrency:
            yield SCRIPTS['navigator_hardware_concurrency']


def stealth_sync(page: SyncPage, config: StealthConfig = None):
    for script in (config or StealthConfig()).enabled_scripts:
        page.add_init_script(script)


async def stealth_async(page: AsyncPage, logger: Logger):
    # options
    max_touch_points: int = 5
    vendor: str = 'Apple Inc.'
    renderer: str = 'Apple GPU'
    nav_vendor: str = 'Apple Computer, Inc.'
    nav_platform: str = 'iPhone'
    hardware_concurrency: int = -1
    #
    opts = json.dumps({
        'webgl_vendor': vendor,
        'webgl_renderer': renderer,
        'navigator_vendor': nav_vendor,
        'navigator_platform': nav_platform,
        'max_touch_points': max_touch_points,
        'hardwareConcurrency': hardware_concurrency,
    })
    await page.add_init_script(f'const opts = {opts}')
    await page.add_init_script(SCRIPTS['utils'])
    await page.add_init_script(SCRIPTS['touchScreen'])
    await page.add_init_script(SCRIPTS['webgl_vendor'])
    await page.add_init_script(SCRIPTS['navigator_vendor'])
    await page.add_init_script(SCRIPTS['navigator_platform'])
    await page.add_init_script(SCRIPTS['navigator_hardware_concurrency'])
