use nonebot;

create table if not exists `user_info` (
    `user_id` bigint(20) not null auto_increment comment '主键自增',
    `user_account` varchar(50) not null default '' comment '用户账号，QQ',
    `region` varchar(50) not null default '+86' comment '地区',
    `mobile_number` varchar(50) not null default '' comment '手机号',
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `status` smallint(2) not null default '1' comment '用户状态，0 - 不可用， 1 - 未激活， 2 - 已激活',
    primary key (`user_id`),
    key `idx_user_account_mobile_number_status` (`user_account`, `mobile_number`, `status`)
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户信息表';

CREATE TABLE IF NOT EXISTS `mobile_verify_code`  (
    code_id bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
    `mobile_number` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '验证码接收号码',
    `verify_code` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '验证码',
    `is_used` tinyint(1) NOT NULL COMMENT '是否使用 0 否 1 是',
    `verify_ip` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '核销IP，方便识别一些机器人账号',
    `expire_at` datetime NOT NULL COMMENT '验证码过期时间',
    `biz_type` tinyint NOT NULL default '0' COMMENT '当前业务',
    `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (code_id) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '验证码核销记录表';