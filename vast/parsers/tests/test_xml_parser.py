from unittest import TestCase


from vast.parsers import xml_parser
from vast.models import vast_v2 as v2_models
from vast import resources


class TestWrapperParser(TestCase):
    def test_simple_wrapper_parsed(self):
        actual = _parse_xml_from_file(resources.SIMPLE_WRAPPER_XML)

        expected = v2_models.Vast.make(
            version="2.0",
            ad=v2_models.Ad.make_wrapper(
                id="70470",
                wrapper=v2_models.Wrapper.make(
                    ad_system="MagU",
                    vast_ad_tag_uri="//vast.dv.com/v3/vast?_vast",
                    ad_title=None,
                    impression="//magu.d.com/vidimp",
                    error="//magu.d.com/viderr?err=[ERRORCODE]",
                    creatives=None,
                ),
            ),
        )
        self.assertEqual(actual, expected)


class TestInlineParser(TestCase):
    def test_simple_inline_parsed(self):
        actual = _parse_xml_from_file(resources.SIMPLE_INLINE_XML)

        expected = v2_models.Vast.make(
            version="2.0",
            ad=v2_models.Ad.make_inline(
                id="509080ATOU",
                inline=v2_models.Inline.make(
                    ad_system="MagU",
                    ad_title="Centers for Disease Control and Prevention: Who Needs a Flu Vaccine",
                    impression="https://mag.dom.com/admy?ad_id=509080ATOU",
                    creatives=[
                        v2_models.Creative.make(
                            linear=v2_models.Linear.make(
                                duration=15,
                                media_files=[
                                    v2_models.MediaFile.make(
                                        asset="https://www.cdc.gov/flu/video/who-needs-flu-vaccine-15_720px.mp4",
                                        delivery="progressive",
                                        type="video/mp4",
                                        bitrate=300,
                                        width=720,
                                        height=420,
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        )
        self.assertEqual(actual, expected)

    def test_inline_multi_media_files_parsed(self):
        actual = _parse_xml_from_file(resources.INLINE_MULTI_FILES_XML)

        expected = v2_models.Vast.make(
            version="2.0",
            ad=v2_models.Ad.make_inline(
                id="509080ATOU",
                inline=v2_models.Inline.make(
                    ad_system="MagU",
                    ad_title="Many Media Files",
                    impression="https://mag.dom.com/admy?ad_id=509080ATOU",
                    creatives=[
                        v2_models.Creative.make(
                            linear=v2_models.Linear.make(
                                duration=15,
                                media_files=[
                                    v2_models.MediaFile.make(
                                        asset="https://vpaid.dv.com/s.swf",
                                        delivery="progressive",
                                        type="application/x-shockwave-flash",
                                        width=176,
                                        height=144,
                                        api_framework="VPAID",
                                    ),
                                    v2_models.MediaFile.make(
                                        asset="https://vpaid.dv.com/js/vpaid-wrapper-dv.js",
                                        delivery="progressive",
                                        type="application/javascript",
                                        width=176,
                                        height=144,
                                        api_framework="VPAID",
                                    ),
                                    v2_models.MediaFile.make(
                                        asset="https://dv.2mdn.net/videoplayback/id/f5316658i7/file.3gpp",
                                        delivery="streaming",
                                        type="video/3gpp",
                                        width=176,
                                        height=144,
                                        min_bitrate=51,
                                        max_bitrate=900,
                                        scalable=False,
                                        maintain_aspect_ratio=False,
                                    ),
                                    v2_models.MediaFile.make(
                                        asset="https://dv.2mdn.net/videoplayback/f5316658i78776/file.3gpp",
                                        delivery="progressive",
                                        type="video/3gpp",
                                        width=320,
                                        height=180,
                                        bitrate=177,
                                        scalable=False,
                                        maintain_aspect_ratio=False,
                                    ),
                                    v2_models.MediaFile.make(
                                        asset="https://dv.2mdn.net/videoplayback/id/f5316658cd737d42/file/file.mp4",
                                        delivery="progressive",
                                        type="video/mp4",
                                        width=640,
                                        height=360,
                                        bitrate=409,
                                        scalable=False,
                                        maintain_aspect_ratio=False,
                                    ),
                                    v2_models.MediaFile.make(
                                        asset="https://dv.2mdn.net/videoplayback/id/f5316658cd737d42/file.webm",
                                        delivery="progressive",
                                        type="video/webm",
                                        bitrate=2452,
                                        width=1280,
                                        height=720,
                                        scalable=False,
                                        maintain_aspect_ratio=False,
                                    ),
                                    v2_models.MediaFile.make(
                                        asset="https://dv.2mdn.net/index.m3u8",
                                        delivery="progressive",
                                        type="application/x-mpegURL",
                                        bitrate=105,
                                        width=256,
                                        height=144,
                                        scalable=False,
                                        maintain_aspect_ratio=False,
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        )
        self.assertEqual(actual, expected)


class TestInlineWithTrackingEvents(TestCase):
    def test_xml_with_tracking(self):
        actual = _parse_xml_from_file(resources.INLINE_WITH_TRACKING_EVENTS_XML)

        expected = v2_models.Vast.make(
            version="2.0",
            ad=v2_models.Ad.make_inline(
                id="509080ATOU",
                inline=v2_models.Inline.make(
                    ad_system="MagU",
                    ad_title="Inline with Tracking Events",
                    impression="https://mag.dom.com/admy?ad_id=509080ATOU",
                    creatives=[
                        v2_models.Creative.make(
                            linear=v2_models.Linear.make(
                                duration=15,
                                media_files=[
                                    v2_models.MediaFile.make(
                                        asset="https://www.cdc.gov/flu/video/who-needs-flu-vaccine-15_720px.mp4",
                                        delivery="progressive",
                                        type="video/mp4",
                                        width=720,
                                        height=420,
                                        bitrate=300,
                                    ),
                                ],
                                tracking_events=[
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri='https://mag.dom.com/vidtrk?evt=creativeView',
                                        tracking_event_type="creativeView"
                                    ),
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri='https://mag.dom.com/vidtrk?evt=start',
                                        tracking_event_type="start"
                                    ),
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri='https://mag.dom.com/vidtrk?evt=midpoint',
                                        tracking_event_type="midpoint"
                                    ),
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri='https://mag.dom.com/vidtrk?evt=firstQuartile',
                                        tracking_event_type="firstQuartile"
                                    ),
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri='https://mag.dom.com/vidtrk?evt=thirdQuartile',
                                        tracking_event_type="thirdQuartile"
                                    ),
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri='https://mag.dom.com/vidtrk?evt=complete',
                                        tracking_event_type="complete"
                                    ),
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri='https://mag.dom.com/vidtrk?evt=mute',
                                        tracking_event_type="mute"
                                    ),
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri='https://mag.dom.com/vidtrk?evt=unmute',
                                        tracking_event_type="unmute"
                                    ),
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri='https://mag.dom.com/vidtrk?evt=rewind',
                                        tracking_event_type="rewind"
                                    ),
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri='https://mag.dom.com/vidtrk?evt=resume',
                                        tracking_event_type="resume"
                                    ),
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri='https://mag.dom.com/vidtrk?evt=fullscreen',
                                        tracking_event_type="fullscreen"
                                    ),
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri='https://mag.dom.com/vidtrk?evt=collapse',
                                        tracking_event_type="collapse"
                                    ),
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri='https://mag.dom.com/vidtrk?evt=acceptInvitation',
                                        tracking_event_type="acceptInvitation"
                                    ),
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri='https://mag.dom.com/vidtrk?evt=close',
                                        tracking_event_type="close"
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        )
        self.assertEqual(actual, expected)

    def test_xml_with_creative_attributes(self):
        actual = _parse_xml_from_file(resources.INLINE_WITH_CREATIVE_ATTRIBUTES)
        expected = v2_models.Vast.make(
            version="2.0",
            ad=v2_models.Ad.make_inline(
                id="509080ATOU",
                inline=v2_models.Inline.make(
                    ad_system="MagU",
                    ad_title="Centers for Disease Control and Prevention: Who Needs a Flu Vaccine",
                    impression="https://mag.dom.com/admy?ad_id=509080ATOU",
                    creatives=[
                        v2_models.Creative.make(
                            linear=v2_models.Linear.make(
                                duration=15,
                                media_files=[
                                    v2_models.MediaFile.make(
                                        asset="https://www.cdc.gov/flu/video/who-needs-flu-vaccine-15_720px.mp4",
                                        delivery="progressive",
                                        type="video/mp4",
                                        bitrate=300,
                                        width=720,
                                        height=420,
                                    ),
                                ],
                            ),
                            id=81997481,
                            sequence=1,
                            ad_id="MagU",
                            api_framework=v2_models.ApiFramework.VPAID,
                        ),
                    ],
                ),
            ),
        )
        self.assertEqual(actual, expected)

    def test_xml_with_video_clicks(self):
        actual = _parse_xml_from_file(resources.INLINE_WITH_VIDEO_CLICKS)

        expected = v2_models.Vast.make(
            version="2.0",
            ad=v2_models.Ad.make_inline(
                id="509080ATOU",
                inline=v2_models.Inline.make(
                    ad_system="MagU",
                    ad_title="Centers for Disease Control and Prevention: Who Needs a Flu Vaccine",
                    impression="https://mag.dom.com/admy?ad_id=509080ATOU",
                    creatives=[
                        v2_models.Creative.make(
                            linear=v2_models.Linear.make(
                                duration=15,
                                media_files=[
                                    v2_models.MediaFile.make(
                                        asset="https://www.cdc.gov/flu/video/who-needs-flu-vaccine-15_720px.mp4",
                                        delivery="progressive",
                                        type="video/mp4",
                                        bitrate=300,
                                        width=720,
                                        height=420,
                                    ),
                                ],
                                video_clicks=v2_models.VideoClicks.make(
                                    click_through="https://mag.dom.com/click_through",
                                    click_tracking="https://mag.dom.com/click_tracking",
                                    custom_click="https://mag.dom.com/custom_click"
                                )
                            ),
                        ),
                    ],
                ),
            ),
        )
        self.assertEqual(actual, expected)

    def test_xml_ad_attributes(self):
        actual = _parse_xml_from_file(resources.INLINE_WITH_AD_PARAMETERS)

        expected = v2_models.Vast.make(
            version="2.0",
            ad=v2_models.Ad.make_inline(
                id="509080ATOU",
                inline=v2_models.Inline.make(
                    ad_system="MagU",
                    ad_title="Centers for Disease Control and Prevention: Who Needs a Flu Vaccine",
                    impression="https://mag.dom.com/admy?ad_id=509080ATOU",
                    creatives=[
                        v2_models.Creative.make(
                            linear=v2_models.Linear.make(
                                duration=15,
                                media_files=[
                                    v2_models.MediaFile.make(
                                        asset="https://www.cdc.gov/flu/video/who-needs-flu-vaccine-15_720px.mp4",
                                        delivery="progressive",
                                        type="video/mp4",
                                        bitrate=300,
                                        width=720,
                                        height=420,
                                    ),
                                ],
                                ad_parameters=v2_models.AdParameters.make(
                                    data="{data : funky data goes here}",
                                    xml_encoded=False,
                                )
                            ),
                        ),
                    ],
                ),
            ),
        )
        self.assertEqual(actual, expected)

    def test_xml_with_non_linear_ads(self):
        actual = _parse_xml_from_file(resources.INLINE_WITH_NON_LINEAR_ADS)

        expected = v2_models.Vast.make(
            version="2.0",
            ad=v2_models.Ad.make_inline(
                id="509080ATOU",
                inline=v2_models.Inline.make(
                    ad_system="MagU",
                    ad_title="Centers for Disease Control and Prevention: Who Needs a Flu Vaccine",
                    impression="https://mag.dom.com/admy?ad_id=509080ATOU",
                    creatives=[
                        v2_models.Creative.make(
                            non_linear=v2_models.NonLinear.make(
                                non_linear_ads=[
                                    v2_models.NonLinearAd.make(
                                        width=100,
                                        height=200,
                                        expanded_width=500,
                                        expanded_height=1000,
                                        scalable=True,
                                        maintain_aspect_ratio=True,
                                        min_suggested_duration=30,
                                        api_framework=v2_models.ApiFramework.VPAID,
                                        id="non_linear_1",
                                        static_resource=v2_models.StaticResource.make(
                                            resource="https://some.static.resource.png",
                                            mime_type="image/png",
                                        ),
                                        iframe_resource="https://some.iframe.resource",
                                        non_linear_click_through=v2_models.UriWithId.make(
                                            resource="https://mag.dom.com/non/linear/click/through",
                                            id="for_fun",
                                        ),
                                    ),
                                    v2_models.NonLinearAd.make(
                                        width=300,
                                        height=700,
                                        scalable=False,
                                        id="non_linear_2",
                                        html_resource="https://some.html.resource.html",
                                        ad_parameters=v2_models.AdParameters.make(
                                            data="{data : funky data goes here}",
                                        )
                                    )
                                ],
                                tracking_events=[
                                    v2_models.TrackingEvent.make(
                                        tracking_event_uri="https://mag.dom.com/vidtrk?evt=creativeView",
                                        tracking_event_type=v2_models.TrackingEventType.CREATIVE_VIEW,
                                    )
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        )
        self.assertEqual(actual, expected)

    def test_xml_with_companions_ads(self):
        actual = _parse_xml_from_file(resources.INLINE_WITH_COMPANION_ADS)

        expected = v2_models.Vast.make(
            version="2.0",
            ad=v2_models.Ad.make_inline(
                id="509080ATOU",
                inline=v2_models.Inline.make(
                    ad_system="MagU",
                    ad_title="Centers for Disease Control and Prevention: Who Needs a Flu Vaccine",
                    impression="https://mag.dom.com/admy?ad_id=509080ATOU",
                    creatives=[
                        v2_models.Creative.make(
                            linear=v2_models.Linear.make(
                                duration=15,
                                media_files=[
                                    v2_models.MediaFile.make(
                                        asset="https://www.cdc.gov/flu/video/who-needs-flu-vaccine-15_720px.mp4",
                                        delivery="progressive",
                                        type="video/mp4",
                                        bitrate=300,
                                        width=720,
                                        height=420,
                                    ),
                                ],
                            ),
                            companion=v2_models.Companion.make(
                                companion_ads=[
                                    v2_models.CompanionAd.make(
                                        width=100,
                                        height=200,
                                        expanded_width=500,
                                        expanded_height=1000,
                                        api_framework=v2_models.ApiFramework.VPAID,
                                        id="companion_ad_1",
                                        static_resource=v2_models.StaticResource.make(
                                            resource="https://some.static.resource.png",
                                            mime_type="image/png",
                                        ),
                                        iframe_resource="https://some.iframe.resource",
                                        companion_click_through="https://mag.dom.com/non/linear/click/through",
                                        tracking_events=[
                                            v2_models.TrackingEvent.make(
                                                tracking_event_uri="https://mag.dom.com/vidtrk?evt=creativeView",
                                                tracking_event_type=v2_models.TrackingEventType.CREATIVE_VIEW,
                                            )
                                        ],
                                        alt_text="This is an alternative text for those who missed that ad",
                                    ),
                                    v2_models.CompanionAd.make(
                                        width=300,
                                        height=700,
                                        id="companion_ad_2",
                                        html_resource="https://some.html.resource.html",
                                        ad_parameters=v2_models.AdParameters.make(
                                            data="{data : funky data goes here}",
                                        )
                                    )
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        )
        self.assertEqual(actual, expected)


def _parse_xml_from_file(path_to_file):
    with open(path_to_file, "r") as fp:
        xml_string = fp.read()

    return xml_parser.from_xml_string(xml_string)


