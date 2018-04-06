## Insight Data Engineering Challenge
### Steps to execute
- Get the code from github
- Go to project root directory and execute the following command from terminal:

    ```
    ./run.sh
    ```
- `run.sh` file contains following python command to execute the `sessionization.py`
     ```
     #!/usr/bin/env bash
      python ./src/sessionization.py ./input/log.csv ./input/inactivity_period.txt ./output/sessionization.txt
     ```

- Output file `sessionization.txt` is created inside **output** folder
- Test cases are maintained in `insight_testsuite` folder
- There are three test cases: _my-test_1_, _my-test_2_, _test_1_
- To execute test cases use following commands
   ```
    cd insight_testsuite
    ./run_tests.sh
   ```
- The test output is maintained in `results.txt` inside _insight_testsuite_.
   ```
    [PASS]: my-test_1 sessionization.txt
    [PASS]: my-test_2 sessionization.txt
    [PASS]: test_1 sessionization.txt
    3 of 3 tests passed
   ```

### Summary of program
- All new IP request is maintained in _activeIpList_, _sortedIpList_ and _ipCollectDict_
- If IP request already exists then update these 3 structures.
- Session expiration is determined by the difference between current time and the last time an IP try to access any document.
- Check the timestamp of each log entry. If a new timestamp is found, check if the session has expired in _sortedIpList_.
- If the session is maintained for the longest seving IP then no need to check remaining IPs
- IPs are removed after session has expired
- Write all remaining entries at the end



#### Developed by [Amit Jha](mailto:amitjha@usc.edu)
