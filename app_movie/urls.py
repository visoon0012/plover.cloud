from rest_framework import routers

from .views import *

router = routers.DefaultRouter()

# router.register(r'company/advertising', AdvertisingCompanyViewset)
# router.register(r'advertising/point', AdvertisingPointViewset)
# router.register(r'company/property', PropertyCompanyViewset)
# router.register(r'community/attribute', CommunityAttributeViewset)
# router.register(r'community/info', CommunityInfoViewset)
# router.register(r'customer/info', CustomerInfoViewset)
# router.register(r'customer/contract', CustomerContractViewset)
# router.register(r'property/contract', PropertyContractViewset)

#
router.register(r'simple', MovieSimpleViewset)
router.register(r'mark', UserMovieSimpleMarkViewset)
router.register(r'resource', MovieResourceViewset)
router.register(r'movie', MovieViewset)
