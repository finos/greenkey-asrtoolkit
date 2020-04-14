#!/usr/bin/env sh

files_to_cleanup="corpus split-corpus split file_conversion_test.txt file_conversion_test.stm json_to_stm_test_2.stm json_to_txt_test.txt json_to_stm_test_1.stm stm_to_srt_test.srt stm_to_vtt_test.vtt stm_to_html_test.html stm_to_txt_test.txt BillGatesTEDTalk_aligned.stm __pycache__"

docker run --rm -it -w /work \
  --user $(id -u):$(id -g) --userns=host \
  -v $PWD:/work asrtoolkit:${TAG:-latest} \
  bash -c 'tests/run_tests.sh'
(cd tests/ && rm -r $files_to_cleanup)
