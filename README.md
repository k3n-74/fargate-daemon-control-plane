# fargate-daemon-control-plane


## API

* StartDaemon
* StopDaemon
* UpdateDaemon
  * task definition
  * fargate platform
* DescribeDaemon
* ListDaemons

## Event

* daemon-started
* daemon-state-illegal-stopped
* daemon-state-recovered
* daemon-stopped
* next-daemon-readied
* old-daemon-stopped

