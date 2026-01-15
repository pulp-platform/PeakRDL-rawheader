
#ifndef TOP_H
#define TOP_H

#define TOP_BASE_ADDR 0x00000000
#define TOP_SIZE 0x00000008


#define TOP_STATUS_BASE_ADDR(status_idx) (0x00000000 + (status_idx * 0x00000004))
#define TOP_STATUS_NUM 0x00000002


#define STATE__IDLE 0
#define STATE__BUSY 1


#endif /* TOP_H */
