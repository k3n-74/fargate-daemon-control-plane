# fargate-daemon-control-plane


## API

### Lambda Functions Interface
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

### Events Interface

* daemon-started
* daemon-state-illegal-stopped
* daemon-state-recovered
* daemon-stopped
* next-daemon-readied
* old-daemon-stopped

previous, current, next
