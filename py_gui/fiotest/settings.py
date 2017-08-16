HOST = 'http://10.240.217.115:8866/api/v2/'

RESULT_COLUMN = [
            {'name': 'jobid'     , 'width': 30},
            # {'name': 'case_name' , 'width': 80},
            {'name': 'time'      , 'width': 20},
            {'name': 'blocksize' , 'width': 10},
            {'name': 'iodepth'   , 'width': 10},
            {'name': 'numberjob' , 'width': 10},
            {'name': 'imagenum'  , 'width': 10},
            {'name': 'clientnum' , 'width': 10},
            {'name': 'readwrite' , 'width': 10},
            {'name': 'r_iops'    , 'width': 10},
            {'name': 'w_iops'    , 'width': 10},
            {'name': 'iops'      , 'width': 10},
            {'name': 'lat'       , 'width': 10},
            {'name': 'r_bw'      , 'width': 10},
            {'name': 'w_bw'      , 'width': 10},
            {'name': 'bw'        , 'width': 10},
            {'name': 'status'    , 'width': 10},
        ]

LEGEND = ['ro-', 'go-', 'bo-', 'co-', 'mo-', 'yo-', 'ko-', 'r*--', 'g*--', 'b*--', 'c*--', 'm*--', 'y*--', 'k*--']
