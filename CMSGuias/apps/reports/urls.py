from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('CMSGuias.apps.reports.views',
	#report test
	url(r'^test/$','view_test_pdf',name='vista_report'),
	# reports
	url(r'^orders/(?P<pid>.*)/(?P<sts>.*)/','rpt_orders_details',name='rpt_orders'),
	url(r'^guidereferral/(?P<gid>.*)/format/','rpt_guide_referral_format',name='rpt_guide_format'),
)