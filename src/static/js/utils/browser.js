/**
 * This function captures detailed information about the user's device,
 * including the user agent, screen dimensions, touch capabilities, platform,
 * browser type, version, and the user's time zone.
 *
 * The following data is captured:
 * - User Agent: The browser and operating system's full user agent string.
 * - Time Zone: The device's time zone via Intl.DateTimeFormat.
 * - Screen Dimensions: The width and height of the screen.
 * - Touchscreen Detection: Whether the device supports touch events.
 * - Platform: The operating system (e.g., Windows, Mac OS, Android, iOS).
 * - Browser Info: Name and version (e.g., Chrome 90.0).
 *
 * @returns {Object} An object with detailed device information.
 */
export default function fingerprintDevice() {
    const userAgent     = navigator.userAgent.toLowerCase();
    const platform      = extractPlatformFromUserAgent(userAgent);
    const isTouchScreen = "ontouchstart" in window || navigator.maxTouchPoints > 0;
    const screenWidth   = window.screen.width;
    const screenHeight  = window.screen.height;
    const pixelRatio    = window.devicePixelRatio || 1

    const browserInfo = userAgent.match(/(chrome|firefox|safari|msie|edge|opera|trident)[\/\s](\d+(\.\d+)?)/i);

    return {
        userAgent: userAgent,
        timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        screenWidth: screenWidth,
        screenHeight: screenHeight,
        isDeviceTouchScreen: isTouchScreen,
        platform: platform,
        browser: browserInfo ? browserInfo[1] : "Unknown Browser",
        browserVersion: browserInfo ? browserInfo[2] : "Unknown Version",
        pixelRatio:pixelRatio,
    };
}


export function extractPlatformFromUserAgent(userAgent) {
    if (!userAgent || typeof userAgent !== "string") {
        throw new Error("Invalid userAgent: The userAgent is either empty or not a string.");
    }

    if (/windows nt/i.test(userAgent)) return "Windows";
    if (/mac os x/i.test(userAgent)) return "Mac OS";
    if (/android/i.test(userAgent)) return "Android";
    if (/iphone|ipad|ipod/i.test(userAgent)) return "iOS";

    return "Unknown Platform";
}
