from datetime import date, datetime
from unittest import TestCase, mock
from unittest.mock import MagicMock

import ornitho
from ornitho import Form, Place, Protocol
from ornitho.api_exception import APIException

ornitho.consumer_key = "ORNITHO_CONSUMER_KEY"
ornitho.consumer_secret = "ORNITHO_CONSUMER_SECRET"
ornitho.user_email = "ORNITHO_USER_EMAIL"
ornitho.user_pw = "ORNITHO_USER_PW"
ornitho.api_base = "ORNITHO_API_BASE"


class TestForm(TestCase):
    def setUp(self):
        self.form_json = {
            "@id": "446171",
            "id_form_universal": "28_446171",
            "time_start": "09:06:00",
            "time_stop": "09:31:00",
            "full_form": "1",
            "version": "0",
            "lat": "52.532542",
            "lon": "13.257572",
            "id_form_mobile": "40232_1583395608201_1",
            "comment": "Begehung 3, 7 Grad , heiter",
            "protocol": {
                "protocol_name": "CBBM",
                "site_code": "DDA-1-Test",
                "local_site_code": "",
                "advanced": "0",
                "visit_number": "158",
                "sequence_number": "1",
                "list_type": "-",
                "wkt": "LINESTRING(8.93297 53.08557, 8.933 53.08559, 8.93291 53.08555, 8.93287 53.08555, 8.93288 53.08556, 8.93289 53.08556, 8.93296 53.08555, 8.93297 53.08555, 8.93298 53.08555, 8.93288 53.08554, 8.93278 53.08554, 8.93261 53.0855, 8.93254 53.08548, 8.9325 53.08545, 8.93243 53.08541, 8.93243 53.08542, 8.93234 53.08534, 8.93225 53.08529, 8.93225 53.08528, 8.9322 53.08528, 8.93215 53.08526, 8.93212 53.08525, 8.93204 53.08523, 8.9319 53.08522, 8.93189 53.08522, 8.93191 53.08523, 8.93189 53.08523, 8.9318 53.08522, 8.93178 53.08521, 8.93167 53.08517, 8.93161 53.08512, 8.9316 53.0851, 8.93161 53.08509, 8.93147 53.08506, 8.93146 53.08506, 8.93145 53.08506, 8.93146 53.08507, 8.93144 53.08507, 8.93131 53.08505, 8.93125 53.08504, 8.93128 53.08503, 8.93125 53.08501, 8.93126 53.08502, 8.93122 53.08502, 8.93116 53.085, 8.93103 53.08497, 8.93098 53.08494, 8.93097 53.08495, 8.93089 53.08493, 8.9308 53.08491, 8.93073 53.08488, 8.93075 53.08491, 8.93068 53.0849, 8.9305 53.08487, 8.93048 53.08486, 8.93049 53.08485, 8.93049 53.08484, 8.93046 53.08484, 8.9304 53.08482, 8.9303 53.08482, 8.93027 53.08481, 8.93026 53.08481, 8.93021 53.08482, 8.93023 53.08481, 8.93021 53.0848, 8.93019 53.0848, 8.93021 53.08479, 8.93018 53.08478, 8.93016 53.08477, 8.93017 53.08477, 8.93006 53.08476, 8.92998 53.08474, 8.92991 53.08473, 8.92988 53.08472, 8.92989 53.0847, 8.9299 53.08471, 8.92991 53.08472, 8.92993 53.08472, 8.92994 53.08471, 8.92981 53.08468, 8.92979 53.0847, 8.92973 53.08469, 8.92971 53.08467, 8.92975 53.08468, 8.92973 53.08464, 8.92973 53.08463, 8.9296 53.08461, 8.92945 53.08461, 8.92943 53.08463, 8.92943 53.08464, 8.9294 53.08462, 8.9294 53.08461, 8.92929 53.08459, 8.92914 53.08457, 8.92895 53.08452, 8.9289 53.08449, 8.92884 53.08449, 8.92882 53.08449, 8.92883 53.08452, 8.92879 53.0845, 8.92868 53.08449, 8.92862 53.08442, 8.92857 53.08441, 8.92852 53.08442, 8.92851 53.08443, 8.92844 53.08441, 8.92843 53.08436, 8.92842 53.08435, 8.92844 53.08434, 8.9284 53.08435, 8.92837 53.08435, 8.92836 53.08434, 8.92832 53.08433, 8.92832 53.08435, 8.92824 53.08433, 8.92804 53.08431, 8.92793 53.08429, 8.92786 53.08425, 8.92776 53.08422, 8.92765 53.0842, 8.92754 53.08416, 8.92747 53.08415, 8.92734 53.08411, 8.92718 53.08407, 8.92702 53.08404, 8.92685 53.08397, 8.92672 53.08395, 8.92662 53.08392, 8.92649 53.0839, 8.92643 53.08387, 8.92642 53.08386, 8.92641 53.08385, 8.92636 53.08383, 8.92619 53.08379, 8.92602 53.08375, 8.92598 53.08374, 8.92599 53.08376, 8.92594 53.08374, 8.92587 53.08372, 8.92552 53.08362, 8.92563 53.08365, 8.92577 53.08369, 8.92593 53.08373, 8.9261 53.08376, 8.9262 53.08377, 8.92621 53.08379, 8.92622 53.08379, 8.9263 53.08381, 8.92644 53.08385, 8.92651 53.08386, 8.92663 53.08389, 8.92662 53.08389, 8.92665 53.08391, 8.92675 53.08394, 8.92693 53.08399, 8.9271 53.08404, 8.92726 53.08407, 8.92744 53.08412, 8.92759 53.08417, 8.92763 53.08418, 8.92775 53.08421, 8.92791 53.08424, 8.9281 53.08426, 8.92813 53.08428, 8.92813 53.08429, 8.92812 53.08429, 8.92811 53.0843, 8.92809 53.08429, 8.9281 53.08431, 8.9281 53.08432, 8.92814 53.08432, 8.92822 53.08435, 8.92836 53.08439, 8.92838 53.08439, 8.92849 53.08438, 8.92858 53.08439, 8.92855 53.08439, 8.92861 53.08441, 8.9286 53.0844, 8.92863 53.08442, 8.92865 53.08442, 8.92863 53.08441, 8.92864 53.08441, 8.92863 53.0844, 8.92866 53.08441, 8.92888 53.08445, 8.92913 53.08451, 8.92917 53.08454, 8.9292 53.08457, 8.92924 53.08455, 8.92922 53.08456, 8.92924 53.08459, 8.92934 53.08464, 8.92952 53.08465, 8.92969 53.0846, 8.92988 53.0845, 8.92993 53.08447, 8.92994 53.08447, 8.93001 53.08442, 8.93003 53.08438, 8.93006 53.08435, 8.93004 53.08434, 8.93019 53.08426, 8.93025 53.08416, 8.93025 53.08413, 8.93026 53.08411, 8.93024 53.08408, 8.93023 53.08407, 8.93024 53.08407, 8.93035 53.08403, 8.93038 53.08399, 8.93045 53.08394, 8.93048 53.08392, 8.93052 53.08389, 8.93057 53.08386, 8.93062 53.08386, 8.93064 53.08385, 8.93063 53.08382, 8.93074 53.08378, 8.93075 53.08373, 8.93073 53.08374, 8.93069 53.08371, 8.93051 53.08368, 8.93039 53.08367, 8.93029 53.08363, 8.93026 53.08361, 8.93024 53.08361, 8.93016 53.08359, 8.93015 53.08359, 8.93014 53.08359, 8.93016 53.08357, 8.93016 53.08356, 8.93015 53.08355, 8.93013 53.08353, 8.93014 53.08351, 8.93012 53.0835, 8.93012 53.08348, 8.93006 53.08339, 8.93005 53.08336, 8.93006 53.08335, 8.93006 53.08334, 8.93005 53.08332, 8.93003 53.08331, 8.92998 53.08333, 8.92998 53.08332, 8.92994 53.08333, 8.92992 53.08332, 8.92991 53.08332, 8.92985 53.08325, 8.92979 53.08315, 8.92974 53.08308, 8.92973 53.08306, 8.92971 53.08303, 8.92969 53.083, 8.9298 53.08293, 8.92991 53.08292, 8.92991 53.08291, 8.93003 53.08292, 8.93016 53.08294, 8.93025 53.08295, 8.93029 53.08296, 8.93047 53.083, 8.93058 53.08301, 8.9306 53.08301, 8.93065 53.08302, 8.93075 53.08307, 8.93077 53.08309, 8.93078 53.08309, 8.93079 53.08309, 8.93078 53.0831, 8.93085 53.08313, 8.93089 53.08313, 8.931 53.08316, 8.931 53.08318, 8.93105 53.08318, 8.93116 53.08322, 8.93121 53.08321, 8.93122 53.08321, 8.93129 53.08321, 8.93138 53.08326, 8.9315 53.08333, 8.93157 53.08337, 8.93158 53.08338, 8.93167 53.0834, 8.93174 53.08342, 8.93181 53.08344, 8.93183 53.08345, 8.93195 53.08346, 8.93211 53.08343, 8.93219 53.08344, 8.93225 53.08345, 8.93232 53.08345, 8.9324 53.08344, 8.93243 53.08345, 8.93242 53.08346, 8.93242 53.08347, 8.93242 53.08348, 8.9324 53.08347, 8.93239 53.08347, 8.93239 53.08347, 8.93239 53.08347, 8.93239 53.08347, 8.93239 53.08347, 8.93239 53.08347, 8.93239 53.08347, 8.93239 53.08347, 8.93239 53.08347, 8.93239 53.08347, 8.93237 53.08347, 8.93238 53.08346, 8.93236 53.08346, 8.93235 53.08345, 8.93235 53.08346, 8.93234 53.08348, 8.93233 53.08351, 8.93248 53.08354, 8.93253 53.08356, 8.93253 53.08355, 8.93266 53.08356, 8.93278 53.08357, 8.93291 53.0836, 8.93298 53.08364, 8.933 53.08366, 8.93301 53.08369, 8.93307 53.08373, 8.93324 53.08377, 8.93331 53.08378, 8.93339 53.08381, 8.93346 53.08382, 8.93359 53.08386, 8.93363 53.08387, 8.93363 53.08386, 8.93376 53.0839, 8.93387 53.08398, 8.93401 53.08405, 8.93409 53.08412, 8.93403 53.08417, 8.93393 53.08421, 8.93378 53.08426, 8.93371 53.08431, 8.93366 53.08434, 8.93358 53.08438, 8.93354 53.08442, 8.93345 53.08448, 8.93337 53.08454, 8.93329 53.08459, 8.93331 53.0846, 8.93321 53.08467, 8.93315 53.08475, 8.9331 53.0848, 8.933 53.0849, 8.93292 53.08501, 8.93284 53.08507, 8.93281 53.08505, 8.93276 53.08516, 8.93267 53.08525, 8.93271 53.08538, 8.93265 53.08545, 8.93261 53.08544, 8.93264 53.08547, 8.93276 53.08552, 8.93279 53.08552, 8.93297 53.08557, 8.93309 53.08559, 8.93309 53.0856, 8.93316 53.08562, 8.93332 53.08566, 8.93351 53.08572, 8.9337 53.08576, 8.93389 53.08581, 8.93408 53.08586, 8.93426 53.0859, 8.93444 53.08595, 8.93456 53.086, 8.93473 53.08604, 8.93484 53.08606, 8.93504 53.0861, 8.93524 53.08615, 8.93537 53.0862, 8.93557 53.08623, 8.93571 53.08623, 8.93589 53.08622, 8.93601 53.08622, 8.93614 53.08621, 8.93624 53.08616, 8.93624 53.08609, 8.93625 53.08608, 8.93624 53.08603, 8.93621 53.08596, 8.93622 53.08593, 8.93622 53.08589, 8.93623 53.08582, 8.93623 53.08576, 8.93622 53.08576, 8.93622 53.08575, 8.93626 53.08567, 8.93628 53.08564, 8.93631 53.08561, 8.9363 53.08562, 8.93628 53.08561, 8.93631 53.08553, 8.93633 53.08547, 8.93634 53.08545, 8.93635 53.08545, 8.93636 53.08541, 8.93636 53.0854, 8.93638 53.08536, 8.9364 53.08531, 8.93641 53.08529, 8.93641 53.08525, 8.93644 53.0852, 8.93647 53.08516, 8.93647 53.08514, 8.93649 53.0851, 8.93649 53.08511, 8.9365 53.0851, 8.93649 53.08512, 8.93652 53.08507, 8.93654 53.085, 8.93654 53.08497, 8.93655 53.08496, 8.93656 53.08496, 8.93657 53.08495, 8.93653 53.08496, 8.93657 53.08488, 8.93659 53.08482, 8.93662 53.08482, 8.93662 53.08481, 8.93663 53.0848, 8.93665 53.08477, 8.93663 53.08475, 8.93665 53.08473, 8.93666 53.08472, 8.93667 53.08469, 8.93668 53.0846, 8.93669 53.08455, 8.93669 53.08454, 8.9367 53.08452, 8.9367 53.0845, 8.93671 53.0845, 8.93671 53.08451, 8.93673 53.08447, 8.93676 53.0844, 8.93675 53.0844, 8.93676 53.08438, 8.93678 53.08432, 8.93677 53.08433, 8.93682 53.08425, 8.93686 53.08415, 8.93687 53.08412, 8.93692 53.08409, 8.93686 53.08409, 8.93688 53.08405, 8.93687 53.08406, 8.93686 53.08405, 8.93685 53.08405, 8.93686 53.08402, 8.93689 53.08401, 8.93695 53.08394, 8.937 53.08384, 8.93703 53.08378, 8.93704 53.08378, 8.93708 53.08377, 8.93713 53.08369, 8.93711 53.08368, 8.93714 53.08362, 8.93717 53.0836, 8.93713 53.08352, 8.93718 53.08344, 8.93718 53.08345, 8.93719 53.08343, 8.93723 53.08339, 8.93725 53.08338, 8.93734 53.0833, 8.93736 53.08326, 8.93735 53.08324, 8.93735 53.08323, 8.93735 53.08322, 8.93729 53.08326, 8.93721 53.08326, 8.93723 53.08327, 8.93724 53.08328, 8.93723 53.08328, 8.93716 53.08326, 8.93714 53.08325, 8.93705 53.08324, 8.93704 53.08322, 8.93694 53.0832, 8.93678 53.08316, 8.9367 53.08315, 8.93669 53.08315, 8.93666 53.08316, 8.93662 53.08311, 8.93659 53.08313, 8.93647 53.08311, 8.93643 53.0831, 8.93641 53.08311, 8.93634 53.08308, 8.93625 53.08304, 8.93619 53.08302, 8.93615 53.083, 8.93619 53.08292, 8.93624 53.08288, 8.9362 53.08288, 8.93628 53.08285, 8.93638 53.08283, 8.93646 53.08276, 8.93651 53.08272, 8.9366 53.08266, 8.93665 53.08262, 8.93675 53.08262, 8.93676 53.0826, 8.93675 53.0826, 8.93685 53.08254, 8.93699 53.08248, 8.93699 53.08247, 8.93703 53.08246, 8.93704 53.08247, 8.93715 53.08241, 8.93721 53.08237, 8.9372 53.08237, 8.9373 53.08233, 8.93729 53.08234, 8.93732 53.08231, 8.93735 53.08229, 8.9374 53.08223, 8.93741 53.08222, 8.93746 53.0822, 8.9375 53.08218, 8.93756 53.08214, 8.93764 53.08207, 8.93769 53.08205, 8.93769 53.08204, 8.93774 53.08203, 8.93774 53.08199, 8.93775 53.08196, 8.93774 53.08196, 8.93776 53.08193, 8.93785 53.08188, 8.93785 53.08187, 8.93787 53.08187, 8.93789 53.08185, 8.93794 53.0818, 8.938 53.08174, 8.93802 53.08174, 8.93807 53.08171, 8.9381 53.08167, 8.93819 53.08159, 8.93829 53.08153, 8.93835 53.08149, 8.93838 53.08149, 8.93843 53.08146, 8.93847 53.08144, 8.93845 53.08145, 8.93848 53.08142, 8.93855 53.08133, 8.93856 53.08133, 8.93864 53.08129, 8.93866 53.08125, 8.93868 53.08123, 8.93875 53.08127, 8.93878 53.08124, 8.93876 53.08121, 8.93879 53.08116, 8.93879 53.0811, 8.93868 53.08103, 8.93862 53.08102, 8.93858 53.08101, 8.93855 53.08102, 8.93854 53.08102, 8.93848 53.081, 8.93847 53.08099, 8.93846 53.08096, 8.93836 53.08094, 8.93824 53.08091, 8.93815 53.08089, 8.938 53.08084, 8.93785 53.0808, 8.9378 53.08081, 8.93781 53.0808, 8.93773 53.08079, 8.9377 53.08079, 8.93763 53.08075, 8.93753 53.08073, 8.93748 53.08071, 8.93733 53.08068, 8.93729 53.08067, 8.9373 53.08068, 8.93718 53.08063, 8.93704 53.08061, 8.93702 53.08061, 8.93695 53.08058, 8.93687 53.08057, 8.93687 53.08058, 8.93683 53.08057, 8.93682 53.08056, 8.93681 53.08055, 8.93671 53.08051, 8.93667 53.0805, 8.93662 53.08048, 8.93659 53.08049, 8.93654 53.08049, 8.93641 53.08044, 8.9363 53.08041, 8.93617 53.08037, 8.9361 53.08035, 8.93606 53.08032, 8.93605 53.08033, 8.93592 53.08028, 8.93583 53.08026, 8.93571 53.08023, 8.9357 53.08023, 8.9357 53.08023, 8.9357 53.08023, 8.9357 53.08023, 8.93569 53.08023, 8.9356 53.0802, 8.93559 53.08019, 8.93558 53.08017, 8.93554 53.08018, 8.93552 53.08019, 8.93544 53.08017, 8.93545 53.08019, 8.93542 53.08019, 8.93541 53.08019, 8.93541 53.08018, 8.9354 53.08018, 8.93532 53.08015, 8.93522 53.08013, 8.93508 53.08009, 8.93504 53.08008, 8.935 53.08008, 8.93491 53.08005, 8.93478 53.08, 8.9348 53.08, 8.93474 53.07998, 8.93475 53.07998, 8.93464 53.07994, 8.9346 53.07994, 8.93457 53.07993, 8.93451 53.07991, 8.93444 53.07987, 8.93444 53.07988, 8.93438 53.07989, 8.93421 53.07985, 8.93408 53.07981, 8.93396 53.07977, 8.93385 53.07974, 8.93379 53.07973, 8.9338 53.07974, 8.93378 53.07972, 8.93373 53.0797, 8.93365 53.07968, 8.93358 53.07967, 8.93347 53.07963, 8.93341 53.07963, 8.93342 53.07964, 8.93329 53.07961, 8.9332 53.07957, 8.93317 53.07956, 8.93307 53.07954, 8.93305 53.0795, 8.93301 53.07951, 8.93288 53.07949, 8.93289 53.07947, 8.93288 53.07948, 8.9328 53.07947, 8.93263 53.07943, 8.93256 53.07939, 8.93239 53.07941, 8.93232 53.07942, 8.93226 53.07942, 8.93223 53.07947, 8.93218 53.07953, 8.93214 53.07961, 8.93212 53.0796, 8.93209 53.07966, 8.93208 53.07966, 8.93209 53.07967, 8.93208 53.07972, 8.93204 53.07972, 8.93201 53.07977, 8.932 53.07983, 8.93198 53.07986, 8.93192 53.07994, 8.93191 53.07996, 8.93191 53.07998, 8.93187 53.08002, 8.93186 53.08004, 8.93178 53.08008, 8.93176 53.08007, 8.93177 53.08008, 8.93177 53.08009, 8.93177 53.0801, 8.93175 53.08011, 8.93168 53.08018, 8.93164 53.08028, 8.93161 53.08035, 8.93172 53.08043, 8.93167 53.08053, 8.9316 53.08062, 8.93154 53.08073, 8.93145 53.08077, 8.9314 53.08077, 8.9314 53.08076, 8.93139 53.08074, 8.93128 53.0808, 8.93119 53.0809, 8.93109 53.08101, 8.93108 53.08103, 8.93105 53.08102, 8.93103 53.08107, 8.93104 53.08107, 8.93105 53.08114, 8.93089 53.08113, 8.93069 53.08107, 8.93049 53.081, 8.93032 53.08096, 8.93024 53.08095, 8.9302 53.08095, 8.93004 53.0809, 8.92988 53.08085, 8.92968 53.0808, 8.92961 53.08077, 8.92947 53.08073, 8.92948 53.08073, 8.92945 53.0807, 8.92935 53.08068, 8.92935 53.08069, 8.92927 53.08067, 8.92907 53.08063, 8.92904 53.08061, 8.92899 53.08061, 8.929 53.0806, 8.92894 53.08059, 8.92873 53.08054, 8.9286 53.08051, 8.92878 53.08056, 8.92898 53.08061, 8.92912 53.08065, 8.9293 53.0807, 8.92947 53.08075, 8.92959 53.08078, 8.92968 53.08081, 8.92973 53.08083, 8.92989 53.08087, 8.92993 53.0809, 8.93012 53.08095, 8.93034 53.08099, 8.93053 53.08105, 8.93069 53.0811, 8.93086 53.08117, 8.93105 53.08122, 8.93116 53.08124, 8.93119 53.08124, 8.93117 53.08123, 8.93118 53.08123, 8.93128 53.08126, 8.93149 53.0813, 8.93166 53.08135, 8.93171 53.08138, 8.9317 53.08137, 8.93181 53.08138, 8.93197 53.08143, 8.9321 53.08147, 8.93219 53.08149, 8.9322 53.08149, 8.9324 53.08154, 8.93254 53.08158, 8.93268 53.08162, 8.93283 53.08167, 8.93292 53.08168, 8.93293 53.08168, 8.93294 53.08168, 8.93295 53.0817, 8.93294 53.0817, 8.93292 53.0817, 8.93294 53.08171, 8.93294 53.08172, 8.93294 53.08173, 8.93284 53.08176, 8.93275 53.0818, 8.9327 53.08183, 8.93257 53.08192, 8.93243 53.08201, 8.93238 53.08204, 8.93233 53.08206, 8.93218 53.08216, 8.93213 53.08219, 8.93199 53.08226, 8.93193 53.08233, 8.93182 53.08238, 8.9317 53.08246, 8.93159 53.08255, 8.93146 53.08266, 8.93131 53.08274, 8.93115 53.08281, 8.93098 53.08287, 8.93082 53.08294, 8.93074 53.08305, 8.9307 53.08307, 8.93071 53.08307, 8.93072 53.08307, 8.93066 53.08315, 8.93068 53.08323, 8.93068 53.08335, 8.93063 53.08346, 8.93055 53.08357, 8.93057 53.08371, 8.93054 53.08382, 8.93043 53.08393, 8.93033 53.08398, 8.93033 53.084, 8.93024 53.08406, 8.93013 53.08409, 8.93013 53.08417, 8.93006 53.08429, 8.92999 53.0844, 8.92999 53.08441, 8.92998 53.08442, 8.92995 53.08443, 8.92985 53.08451, 8.92975 53.0846, 8.92982 53.08466, 8.92987 53.08469, 8.92996 53.0847, 8.92997 53.0847, 8.93003 53.08474, 8.93007 53.08474, 8.93014 53.08476, 8.93022 53.08478, 8.93033 53.08481, 8.93044 53.08482, 8.93062 53.08487, 8.9308 53.08491, 8.93083 53.08492, 8.9309 53.08493, 8.93104 53.08495, 8.93118 53.08498, 8.93128 53.085, 8.93141 53.08505, 8.9314 53.08505, 8.93153 53.08509, 8.93157 53.08511, 8.93157 53.08513, 8.9316 53.08514, 8.93171 53.08519, 8.93186 53.08523, 8.93191 53.08522, 8.93197 53.08524, 8.93216 53.08528, 8.93235 53.08532, 8.9325 53.08538, 8.93265 53.08546, 8.93276 53.08551, 8.93282 53.08552)",
                "waterbird_conditions": "GOOD_NORMAL",
                "waterbird_coverage": "COMPLETE",
                "waterbird_optical": "TELESCOPE",
                "waterbird_countmethod": "GROUND",
                "waterbird_ice": "NO_ICE",
                "waterbird_waterlevel": "NO_SNOW",
                "waterbird_snowcover": "NO_SNOW",
                "waterbird_counttype": "NORMAL",
                "waterbird_visibility": "NORMAL",
                "waterbird_waves": "NORMAL",
                "waterbird_conditions_reason": "NORMAL",
                "waterbird_count_payed": "NORMAL",
                "waterbird_activity_persons_on_shore": "NORMAL",
                "waterbird_activity_boats_rowing": "NORMAL",
                "waterbird_activity_boats_motor": "NORMAL",
                "waterbird_activity_boats_sailing": "NORMAL",
                "waterbird_activity_boats_kayak": "NORMAL",
                "waterbird_activity_boats_fisherman": "NORMAL",
                "waterbird_activity_divers": "NORMAL",
                "waterbird_activity_surfers": "NORMAL",
                "moving_harvest": "NORMAL",
                "coverage": "NORMAL",
                "condition": "NORMAL",
                "chiro_identify": "NORMAL",
                "additional_observer": "NORMAL",
                "changes": "NORMAL",
                "drone_used": "NORMAL",
                "tmp_water_bodies": "NORMAL",
            },
            "sightings": [
                {
                    "date": {
                        "@notime": "1",
                        "@offset": "3600",
                        "@timestamp": "1583362800",
                    },
                    "species": {
                        "@id": "385",
                        "taxonomy": "1",
                        "rarity": "verycommon",
                        "category": "C",
                    },
                    "place": {
                        "@id": "822442",
                        "id_universal": "28_45114715",
                        "place_type": "transect",
                        "name": "DDA-Teststrecke Münster",
                        "lat": "51.99666467623097",
                        "lon": "7.6341611553058595",
                        "loc_precision": "0",
                    },
                    "observers": [
                        {
                            "@id": "3277",
                            "@uid": "40232",
                            "traid": "3277",
                            "id_sighting": "45114715",
                            "id_universal": "28_45114715",
                            "guid": "c97731f4-5ebb-41ea-805a-01c002b0655b",
                            "version": "0",
                            "timing": {
                                "@notime": "0",
                                "@offset": "3600",
                                "@timestamp": "1583396828",
                            },
                            "coord_lat": "52.532542",
                            "coord_lon": "13.257572",
                            "altitude": "32",
                            "id_form": "446171",
                            "id_form_universal": "28_446171",
                            "precision": "transect_precise",
                            "estimation_code": "EXACT_VALUE",
                            "count": "1",
                            "flight_number": "1",
                            "hidden": "1",
                            "source": "WEB",
                            "insert_date": "1583397121",
                            "atlas_code": "3",
                        }
                    ],
                },
            ],
        }
        self.form = Form.create_from_ornitho_json(self.form_json)

    def test_instance_url(self):
        self.assertEqual("observations/search", self.form.instance_url())

    @mock.patch("ornitho.model.form.APIRequester")
    def test_refresh(self, mock_requester):
        class MockRequesterClass:
            def request_raw(self, method, url, short_version, body):
                return {"data": {"forms": [{"time_start": "01:01:01"}]}}, None

        def enter_requester(requester):
            return MockRequesterClass()

        mock_requester.return_value.__enter__ = enter_requester
        form = self.form.refresh()
        self.assertEqual("01:01:01", form.time_start.strftime("%H:%M:%S"))

    @mock.patch("ornitho.model.form.APIRequester")
    def test_refresh_exception(self, mock_requester):
        class MockRequesterClass:
            def request_raw(self, method, url, short_version, body):
                return {"data": {"WRONG": [{"time_start": "NEW"}]}}, None

        def enter_requester(requester):
            return MockRequesterClass()

        mock_requester.return_value.__enter__ = enter_requester
        self.assertRaises(
            APIException,
            lambda: self.form.refresh(),
        )

    def test_id_form_universal(self):
        self.assertEqual(
            self.form_json["id_form_universal"],
            self.form.id_form_universal,
        )

    def test_day(self):
        form_json = {
            "@id": "1",
            "day": {"@timestamp": "1583396828"},
        }
        self.assertEqual(
            date.fromtimestamp(
                int(self.form_json["sightings"][0]["date"]["@timestamp"])
            ),
            Form.create_from_ornitho_json(form_json).day,
        )

        self.assertEqual(
            date.fromtimestamp(
                int(self.form_json["sightings"][0]["date"]["@timestamp"])
            ),
            self.form.day,
        )

        with mock.patch("ornitho.model.Form.refresh") as mock_refresh:
            self.assertIsNone(Form().day)
            mock_refresh.assert_called_once()

    def test_time_start(self):
        self.assertEqual(
            self.form_json["time_start"],
            self.form.time_start.strftime("%H:%M:%S"),
        )
        new_time = datetime.now().time()
        self.form.time_start = new_time
        self.assertEqual(
            new_time.replace(microsecond=0),
            self.form.time_start,
        )

    def test_time_stop(self):
        self.assertEqual(
            self.form_json["time_stop"],
            self.form.time_stop.strftime("%H:%M:%S"),
        )
        new_time = datetime.now().time()
        self.form.time_stop = new_time
        self.assertEqual(
            new_time.replace(microsecond=0),
            self.form.time_stop,
        )

    def test_full_form(self):
        self.assertEqual(
            False if self.form_json["full_form"] == "0" else True, self.form.full_form
        )
        self.form.full_form = True
        self.assertTrue(self.form.full_form)
        self.form.full_form = False
        self.assertFalse(self.form.full_form)

    def test_version(self):
        self.assertEqual(
            int(self.form_json["version"]),
            self.form.version,
        )

    def test_lat(self):
        self.assertEqual(
            float(self.form_json["lat"]),
            self.form.lat,
        )

    def test_lon(self):
        self.assertEqual(
            float(self.form_json["lon"]),
            self.form.lon,
        )

    def test_id_form_mobile(self):
        self.assertEqual(
            self.form_json["id_form_mobile"],
            self.form.id_form_mobile,
        )

    def test_comment(self):
        self.assertEqual(
            self.form_json["comment"],
            self.form.comment,
        )

        form = Form()
        form.comment = "COMMENT"
        self.assertEqual("COMMENT", form.comment)

    def test_protocol_name(self):
        self.assertEqual(
            self.form_json["protocol"]["protocol_name"],
            self.form.protocol_name,
        )

        self.form.protocol_name = "NEW_PROTOCOL"
        self.assertEqual("NEW_PROTOCOL", self.form.protocol_name)

        new_form = Form()
        new_form.protocol_name = "NEW_PROTOCOL_2"
        self.assertEqual("NEW_PROTOCOL_2", new_form.protocol_name)

    def test_site_code(self):
        self.assertEqual(
            self.form_json["protocol"]["site_code"],
            self.form.site_code,
        )

        self.form.site_code = "SITE_CODE"
        self.assertEqual("SITE_CODE", self.form.site_code)

        new_form = Form()
        new_form.site_code = "SITE_CODE_2"
        self.assertEqual("SITE_CODE_2", new_form.site_code)

    def test_local_site_code(self):
        self.assertEqual(
            self.form_json["protocol"]["local_site_code"],
            self.form.local_site_code,
        )

    def test_advanced(self):
        self.assertEqual(
            False if self.form_json["protocol"]["advanced"] == "0" else True,
            self.form.advanced,
        )

    def test_visit_number(self):
        self.assertEqual(
            int(self.form_json["protocol"]["visit_number"]),
            self.form.visit_number,
        )

        self.form.visit_number = 99
        self.assertEqual(99, self.form.visit_number)

        new_form = Form()
        new_form.visit_number = 999
        self.assertEqual(999, new_form.visit_number)

    def test_sequence_number(self):
        self.assertEqual(
            int(self.form_json["protocol"]["sequence_number"]),
            self.form.sequence_number,
        )

        self.form.sequence_number = 99
        self.assertEqual(99, self.form.sequence_number)

        new_form = Form()
        new_form.sequence_number = 999
        self.assertEqual(999, new_form.sequence_number)

    def test_list_type(self):
        self.assertEqual(
            self.form_json["protocol"]["list_type"],
            self.form.list_type,
        )

    def test_wkt(self):
        self.assertEqual(
            self.form_json["protocol"]["wkt"],
            self.form.wkt,
        )

    def test_id_waterbird_conditions(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_conditions"],
            self.form.id_waterbird_conditions,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_conditions": {
                    "@id": "GOOD_NORMAL",
                    "#text": "günstig / normal",
                },
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_conditions"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_conditions,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_conditions
        )

        form = Form()
        form.id_waterbird_conditions = "1"
        self.assertEqual("1", form.id_waterbird_conditions)
        form.id_waterbird_conditions = "2"
        self.assertEqual("2", form.id_waterbird_conditions)

    def test_id_waterbird_coverage(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_coverage"],
            self.form.id_waterbird_coverage,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_coverage": {"@id": "COMPLETE", "#text": "± vollständig"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_coverage"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_coverage,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_coverage
        )

    def test_id_waterbird_optical(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_optical"],
            self.form.id_waterbird_optical,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_optical": {"@id": "TELESCOPE", "#text": "Spektiv"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_optical"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_optical,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(Form.create_from_ornitho_json(form_json).id_waterbird_optical)

    def test_id_waterbird_countmethod(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_countmethod"],
            self.form.id_waterbird_countmethod,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_countmethod": {
                    "@id": "GROUND",
                    "#text": "Boden (Auto, Fahrrad, zu Fuß)",
                },
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_countmethod"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_countmethod,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_countmethod
        )

    def test_id_waterbird_ice(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_ice"],
            self.form.id_waterbird_ice,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_ice": {"@id": "NO_ICE", "#text": "kein Eis"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_ice"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_ice,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(Form.create_from_ornitho_json(form_json).id_waterbird_ice)

    def test_id_waterbird_snowcover(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_snowcover"],
            self.form.id_waterbird_snowcover,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_snowcover": {"@id": "NO_SNOW", "#text": "kein Schnee"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_snowcover"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_snowcover,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_snowcover
        )

    def test_id_waterbird_waterlevel(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_waterlevel"],
            self.form.id_waterbird_waterlevel,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_waterlevel": {"@id": "NO_SNOW", "#text": "kein Schnee"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_waterlevel"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_waterlevel,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_waterlevel
        )

    def test_id_waterbird_counttype(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_counttype"],
            self.form.id_waterbird_counttype,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_counttype": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_counttype"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_counttype,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_counttype
        )

    def test_id_waterbird_visibility(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_visibility"],
            self.form.id_waterbird_visibility,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_visibility": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_visibility"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_visibility,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_visibility
        )

    def test_id_waterbird_waves(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_waves"],
            self.form.id_waterbird_waves,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_waves": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_waves"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_waves,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(Form.create_from_ornitho_json(form_json).id_waterbird_waves)

    def test_id_waterbird_conditions_reason(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_conditions_reason"],
            self.form.id_waterbird_conditions_reason,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_conditions_reason": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_conditions_reason"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_conditions_reason,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_conditions_reason
        )

    def test_id_waterbird_count_payed(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_count_payed"],
            self.form.id_waterbird_count_payed,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_count_payed": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_count_payed"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_count_payed,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_count_payed
        )

    def test_id_waterbird_activity_persons_on_shore(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_activity_persons_on_shore"],
            self.form.id_waterbird_activity_persons_on_shore,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_activity_persons_on_shore": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_activity_persons_on_shore"]["@id"],
            Form.create_from_ornitho_json(
                form_json
            ).id_waterbird_activity_persons_on_shore,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(
                form_json
            ).id_waterbird_activity_persons_on_shore
        )

    def test_id_waterbird_activity_boats_rowing(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_activity_boats_rowing"],
            self.form.id_waterbird_activity_boats_rowing,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_activity_boats_rowing": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_activity_boats_rowing"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_activity_boats_rowing,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_activity_boats_rowing
        )

    def test_id_waterbird_activity_boats_motor(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_activity_boats_motor"],
            self.form.id_waterbird_activity_boats_motor,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_activity_boats_motor": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_activity_boats_motor"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_activity_boats_motor,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_activity_boats_motor
        )

    def test_id_waterbird_activity_boats_sailing(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_activity_boats_sailing"],
            self.form.id_waterbird_activity_boats_sailing,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_activity_boats_sailing": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_activity_boats_sailing"]["@id"],
            Form.create_from_ornitho_json(
                form_json
            ).id_waterbird_activity_boats_sailing,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_activity_boats_sailing
        )

    def test_id_waterbird_activity_boats_kayak(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_activity_boats_kayak"],
            self.form.id_waterbird_activity_boats_kayak,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_activity_boats_kayak": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_activity_boats_kayak"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_activity_boats_kayak,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_activity_boats_kayak
        )

    def test_id_waterbird_activity_boats_fisherman(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_activity_boats_fisherman"],
            self.form.id_waterbird_activity_boats_fisherman,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_activity_boats_fisherman": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_activity_boats_fisherman"]["@id"],
            Form.create_from_ornitho_json(
                form_json
            ).id_waterbird_activity_boats_fisherman,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(
                form_json
            ).id_waterbird_activity_boats_fisherman
        )

    def test_id_waterbird_activity_divers(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_activity_divers"],
            self.form.id_waterbird_activity_divers,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_activity_divers": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_activity_divers"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_activity_divers,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_activity_divers
        )

    def test_id_waterbird_activity_surfers(self):
        self.assertEqual(
            self.form_json["protocol"]["waterbird_activity_surfers"],
            self.form.id_waterbird_activity_surfers,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "waterbird_activity_surfers": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["waterbird_activity_surfers"]["@id"],
            Form.create_from_ornitho_json(form_json).id_waterbird_activity_surfers,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_waterbird_activity_surfers
        )

    def test_id_moving_harvest(self):
        self.assertEqual(
            self.form_json["protocol"]["moving_harvest"],
            self.form.id_moving_harvest,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "moving_harvest": {"@id": "MAINLY", "#text": "Überwiegend (>50 %) "},
            },
        }
        self.assertEqual(
            form_json["protocol"]["moving_harvest"]["@id"],
            Form.create_from_ornitho_json(form_json).id_moving_harvest,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(Form.create_from_ornitho_json(form_json).id_moving_harvest)

    def test_id_coverage(self):
        self.assertEqual(
            self.form_json["protocol"]["coverage"],
            self.form.id_coverage,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "coverage": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["coverage"]["@id"],
            Form.create_from_ornitho_json(form_json).id_coverage,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(Form.create_from_ornitho_json(form_json).id_coverage)

    def test_id_condition(self):
        self.assertEqual(
            self.form_json["protocol"]["condition"],
            self.form.id_condition,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "condition": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["condition"]["@id"],
            Form.create_from_ornitho_json(form_json).id_condition,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(Form.create_from_ornitho_json(form_json).id_condition)

    def test_id_chiro_identify(self):
        self.assertEqual(
            self.form_json["protocol"]["chiro_identify"],
            self.form.id_chiro_identify,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "chiro_identify": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["chiro_identify"]["@id"],
            Form.create_from_ornitho_json(form_json).id_chiro_identify,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(Form.create_from_ornitho_json(form_json).id_chiro_identify)

    def test_id_additional_observer(self):
        self.assertEqual(
            self.form_json["protocol"]["additional_observer"],
            self.form.id_additional_observer,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "additional_observer": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["additional_observer"]["@id"],
            Form.create_from_ornitho_json(form_json).id_additional_observer,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(
            Form.create_from_ornitho_json(form_json).id_additional_observer
        )

    def test_id_changes(self):
        self.assertEqual(
            self.form_json["protocol"]["changes"],
            self.form.id_changes,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "changes": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["changes"]["@id"],
            Form.create_from_ornitho_json(form_json).id_changes,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(Form.create_from_ornitho_json(form_json).id_changes)

    def test_id_drone_used(self):
        self.assertEqual(
            self.form_json["protocol"]["drone_used"],
            self.form.id_drone_used,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "drone_used": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["drone_used"]["@id"],
            Form.create_from_ornitho_json(form_json).id_drone_used,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(Form.create_from_ornitho_json(form_json).id_drone_used)

    def test_id_tmp_water_bodies(self):
        self.assertEqual(
            self.form_json["protocol"]["tmp_water_bodies"],
            self.form.id_tmp_water_bodies,
        )

        form_json = {
            "@id": "1",
            "protocol": {
                "tmp_water_bodies": {"@id": "TEST", "#text": "test"},
            },
        }
        self.assertEqual(
            form_json["protocol"]["tmp_water_bodies"]["@id"],
            Form.create_from_ornitho_json(form_json).id_tmp_water_bodies,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(Form.create_from_ornitho_json(form_json).id_tmp_water_bodies)

    def test_playbacks(self):
        self.assertIsNone(self.form.playbacks)

        form_json = {
            "@id": "1",
            "protocol": {
                "playback": {
                    "Id_species_1": "1",
                    "Id_species_2": "0",
                },
            },
        }
        self.assertEqual(
            {1: True, 2: False},
            Form.create_from_ornitho_json(form_json).playbacks,
        )

        form_json = {"@id": "1"}
        self.assertIsNone(Form.create_from_ornitho_json(form_json).playbacks)

    @mock.patch("ornitho.model.observation.Observation")
    def test_observations(self, mock_observation):
        self.form.refresh = MagicMock(return_value=self.form_json)
        mock_observation.create_from_ornitho_json.return_value = "Observation"
        observations = self.form.observations
        mock_observation.create_from_ornitho_json.assert_called_with(
            self.form_json["sightings"][0]
        )
        self.assertEqual(observations, ["Observation"])

        del self.form_json["sightings"]
        self.form.refresh = MagicMock(return_value=self.form_json)
        mock_observation.create_from_ornitho_json.return_value = "Observation"
        observations = self.form.observations
        self.assertEqual(observations, ["Observation"])

        self.form.observations = [mock_observation()]
        self.form.id_place = None
        self.form.observations = [mock_observation()]

    def test_playblack_played(self):
        mock_species = mock.MagicMock(spec=ornitho.Species)
        type(mock_species).id_ = mock.PropertyMock(return_value=1)
        self.assertEqual(mock_species.id_, 1)
        self.assertIsNone(self.form.playblack_played(1))
        self.assertIsNone(self.form.playblack_played(mock_species))

        form_json = {
            "@id": "1",
            "protocol": {
                "playback": {
                    "Id_species_1": "1",
                    "Id_species_2": "0",
                },
            },
        }
        self.assertTrue(Form.create_from_ornitho_json(form_json).playblack_played(1))
        self.assertFalse(Form.create_from_ornitho_json(form_json).playblack_played(2))
        self.assertTrue(
            Form.create_from_ornitho_json(form_json).playblack_played(mock_species)
        )

    @mock.patch("ornitho.model.form.Observation")
    @mock.patch("ornitho.model.form.CreateableModel.get")
    @mock.patch("ornitho.model.form.CreateableModel.create_in_ornitho")
    def test_create(self, mock_create_in_ornitho, mock_get, mock_observation):
        mock_create_in_ornitho.return_value = 1
        id_form_mock = MagicMock()
        id_form_mock.id_form.return_value = 1
        mock_get.return_value = id_form_mock
        mock_observation.raw_data_trim_field_ids.return_value = "TRIMMED!"

        Form.create(
            time_start=datetime.now().time(),
            time_stop=datetime.now().time(),
            observations=[mock_observation],
            protocol="PROTOCOL",
            place=1,
            visit_number=250,
            sequence_number=100,
        )
        mock_create_in_ornitho.assert_called()
        mock_observation.raw_data_trim_field_ids.assert_called()

        Form.create(
            time_start=datetime.now().time(),
            time_stop=datetime.now().time(),
            observations=[mock_observation],
            protocol=mock.Mock(spec=Protocol),
            place=mock.Mock(spec=Place),
            visit_number=250,
            sequence_number=100,
            comment="COMMENT",
        )
        mock_create_in_ornitho.assert_called()
        mock_observation.raw_data_trim_field_ids.assert_called()

        Form.create(
            time_start=datetime.now().time(),
            time_stop=datetime.now().time(),
            observations=[mock_observation],
            protocol=mock.Mock(spec=Protocol),
            place=mock.Mock(spec=Place),
            visit_number=250,
            sequence_number=100,
            create_in_ornitho=False,
            id_waterbird_conditions="1",
        )
        mock_create_in_ornitho.assert_called()
        mock_observation.raw_data_trim_field_ids.assert_called()
