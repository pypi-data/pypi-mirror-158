const override = {
    userAgent:
        this.opts.userAgent ||
        (await page.browser().userAgent()).replace(
            'HeadlessChrome/',
            'Chrome/'
        ),
    acceptLanguage: this.opts.locale || 'en-US,en',
    platform: this.opts.platform
}

page._client.send('Network.setUserAgentOverride', override)