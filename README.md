# fargate-daemon-control-plane


## API

### Lambda Function Interface
* StartDaemon
* StopDaemon
* PrepareSwapDaemon
  * daemon id
  * task definition
  * fargate platform
* CompleteSwapDaemon
  * daemon id
  * task definition
  * fargate platform
* DescribeDaemon
* ListDaemons

## Event Interface

* daemon-started
* daemon-state-illegal-stopped
* daemon-state-recovered
* daemon-stopped
* next-daemon-readied
* old-daemon-stopped

previous, current, next
