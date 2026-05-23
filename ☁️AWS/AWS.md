
---

# Table of Contents

- [[#What is AWS?]]
- [[#Global Infrastructure]]
- [[#IAM]]
- [[#EC2]]
- [[#EBS]]
- [[#S3]]
- [[#VPC]]
- [[#Security Groups vs NACL]]
- [[#Route 53]]
- [[#Load Balancers]]
- [[#Auto Scaling]]
- [[#RDS]]
- [[#ElastiCache]]
- [[#CloudWatch]]
- [[#CloudTrail]]
- [[#AWS CLI]]
- [[#Infrastructure as Code]]
- [[#Containers on AWS]]
- [[#Serverless]]
- [[#Storage Services]]
- [[#Networking Deep Dive]]
- [[#Cost Management]]
- [[#Security Best Practices]]
- [[#🚑 Real-World Scenarios]]
- [[#Interview Questions]]
- [[#Practice Labs]]
- [[#Learning Roadmap]]

---

# What is AWS?

AWS (Amazon Web Services) is the world's most comprehensive cloud platform, launched in 2006 by Amazon. Instead of buying physical servers, you rent infrastructure on demand.

**Core model:**

- **Pay-as-you-go** — pay only for what you use
- **On-demand** — provision in seconds, not weeks
- **Global** — 30+ regions, 90+ availability zones
- **Managed** — AWS handles hardware, patching, datacenters

**Used for:**

- Web hosting & applications
- DevOps pipelines (CI/CD)
- Machine learning & AI
- Big data & analytics
- Databases (managed)
- Kubernetes & containers
- Disaster recovery
- IoT

**AWS vs Azure vs GCP:**

|Feature|AWS|Azure|GCP|
|---|---|---|---|
|Market share|~33% (leader)|~22%|~11%|
|Compute|EC2|Azure VMs|Compute Engine|
|Kubernetes|EKS|AKS|GKE|
|Object storage|S3|Blob Storage|Cloud Storage|
|Serverless|Lambda|Azure Functions|Cloud Functions|
|Best for|Breadth, maturity|Enterprise/Microsoft|Data, ML|

---

# Global Infrastructure

## Regions

A **Region** is a geographic area containing multiple isolated data centers.

```
ap-south-1       → Mumbai, India
us-east-1        → N. Virginia, USA (oldest, most services)
eu-west-1        → Ireland
ap-southeast-1   → Singapore
us-west-2        → Oregon
```

**How to choose a region:**

1. **Latency** — closest to your users
2. **Compliance** — data residency laws (GDPR, etc.)
3. **Service availability** — not all services in all regions
4. **Cost** — prices vary by region (us-east-1 often cheapest)

---

## Availability Zones (AZ)

Each region has **2–6 AZs**. Each AZ is one or more physical data centers with independent power, cooling, and networking.

```
ap-south-1 (Mumbai)
├── ap-south-1a  ← Data center A
├── ap-south-1b  ← Data center B
└── ap-south-1c  ← Data center C
```

**Why multiple AZs matter:**

- If ap-south-1a goes down → your app still runs in 1b and 1c
- This is **High Availability (HA)**
- Always deploy production across ≥ 2 AZs

---

## Edge Locations & CloudFront

**Edge locations** (~450+ globally) cache content closer to users.

```
User in Chennai
    ↓
Edge Location (Chennai)  ← cache hit → returns instantly
    ↓ (cache miss)
CloudFront origin (S3 / EC2 / ALB)
```

**Services using edge locations:**

- CloudFront (CDN)
- Route 53 (DNS)
- AWS Shield (DDoS protection)
- AWS WAF

---

## AWS Well-Architected Framework

5 pillars every AWS architect should know:

|Pillar|Focus|
|---|---|
|Operational Excellence|Automate, monitor, improve|
|Security|IAM, encryption, detection|
|Reliability|Multi-AZ, backup, recovery|
|Performance Efficiency|Right-sizing, caching|
|Cost Optimization|Pay only for what you use|

---

# IAM (Identity and Access Management)

IAM is the **security backbone of AWS**. It controls who can do what in your account. It's global (not region-specific).

---

## IAM Components

|Component|Purpose|Example|
|---|---|---|
|Root User|Full account owner|Never use day-to-day|
|IAM User|Individual identity|`loki@company.com`|
|IAM Group|Collection of users|`developers`, `admins`|
|IAM Role|Temporary assumed identity|EC2 accessing S3|
|Policy|JSON document defining permissions|Allow s3:GetObject|

---

## How IAM Works

```
Principal (Who?)
    ↓
Authentication (Is it really them?)
    ↓
Authorization — check Policy (What can they do?)
    ↓
Action on Resource
```

---

## IAM Policy Structure

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowS3ReadOnly",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-bucket",
        "arn:aws:s3:::my-bucket/*"
      ],
      "Condition": {
        "StringEquals": {
          "aws:RequestedRegion": "ap-south-1"
        }
      }
    }
  ]
}
```

**Policy evaluation logic:**

```
Default: DENY everything
    ↓
Explicit ALLOW in policy → allow
    ↓
Explicit DENY anywhere → deny (overrides allow)
```

---

## Types of Policies

|Type|Attached To|Use|
|---|---|---|
|AWS Managed|Users/Groups/Roles|Predefined by AWS|
|Customer Managed|Users/Groups/Roles|Your custom policies|
|Inline Policy|One specific entity|Strict 1:1 binding|
|Resource Policy|S3, SQS, Lambda|Who can access the resource|
|Permission Boundary|User or Role|Max permissions cap|

---

## IAM Roles — The Right Way to Grant Access

Never use access keys inside EC2. Use IAM Roles.

```
EC2 Instance
    ↓ (has attached IAM Role: "ec2-s3-read-role")
    ↓ (role has policy: AllowS3Read)
    ↓
Can read S3 without any hardcoded credentials
```

```bash
# On EC2 with role — no keys needed
aws s3 ls s3://my-bucket/

# Metadata service provides temp credentials
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
```

---

## IAM Best Practices

```
✅ Lock away root account (use MFA, don't create access keys)
✅ Create individual IAM users (no sharing)
✅ Use Groups to assign permissions
✅ Use Roles for services (EC2, Lambda, ECS)
✅ Enable MFA for all users
✅ Rotate access keys regularly (or better: use roles)
✅ Use least privilege
✅ Use IAM Access Analyzer to find unused permissions
✅ Enable CloudTrail to audit IAM activity
```

```bash
# CLI: Create user + group + attach policy
aws iam create-user --user-name loki
aws iam create-group --group-name developers
aws iam add-user-to-group --user-name loki --group-name developers
aws iam attach-group-policy \
  --group-name developers \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# List who has access to what
aws iam generate-credential-report
aws iam get-credential-report
```

---

# EC2 (Elastic Compute Cloud)

EC2 is a **virtual machine** (server) in the AWS cloud. It's the foundation of most AWS architectures.

---

## EC2 Core Components

|Component|What It Is|Analogy|
|---|---|---|
|AMI|VM template (OS + pre-installed software)|ISO image|
|Instance Type|CPU + RAM size|Server hardware spec|
|EBS|Persistent storage|Hard drive|
|Security Group|Firewall rules|Firewall|
|Key Pair|SSH public/private key|SSH key|
|Elastic IP|Static public IP|Fixed IP address|
|User Data|Startup script|Cloud-init script|

---

## Instance Type Families

```
t  → Burstable (general purpose, dev/test)
m  → Memory balanced (general purpose, prod)
c  → Compute optimized (CPU-heavy workloads)
r  → Memory optimized (databases, caches)
i  → Storage optimized (high IOPS)
g  → GPU (ML training, graphics)
p  → GPU (high performance ML)
```

|Instance|vCPU|RAM|Use Case|
|---|---|---|---|
|t3.micro|2|1 GB|Free tier, testing|
|t3.small|2|2 GB|Small apps|
|t3.medium|2|4 GB|Dev environments|
|m5.large|2|8 GB|General prod|
|m5.xlarge|4|16 GB|Web servers|
|c5.xlarge|4|8 GB|CPU-intensive|
|r5.large|2|16 GB|Databases, Redis|
|i3.large|2|15 GB|High IOPS storage|

---

## EC2 Pricing Models

|Model|Cost|Best For|
|---|---|---|
|On-Demand|Highest|Unpredictable workloads, testing|
|Reserved (1yr/3yr)|Up to 72% off|Steady-state production|
|Spot|Up to 90% off|Batch jobs, fault-tolerant|
|Savings Plans|Up to 66% off|Flexible commitment|
|Dedicated Host|Highest|Licensing, compliance|

```
💡 Tip: Use On-Demand for dev/test, Reserved for prod baseline,
        Spot for batch processing / CI runners.
```

---

## EC2 Lifecycle

```
Stopped ──► Pending ──► Running ──► Stopping ──► Stopped
                           │
                           └──► Shutting down ──► Terminated
```

```bash
# Common EC2 CLI commands
aws ec2 describe-instances
aws ec2 start-instances --instance-ids i-1234567890abcdef0
aws ec2 stop-instances --instance-ids i-1234567890abcdef0
aws ec2 reboot-instances --instance-ids i-1234567890abcdef0
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0

# Get public IP of instance
aws ec2 describe-instances \
  --query 'Reservations[*].Instances[*].PublicIpAddress' \
  --output text
```

---

## User Data (Startup Script)

Runs once on first boot. Used to auto-configure instances.

```bash
#!/bin/bash
apt update -y
apt install -y nginx
systemctl start nginx
systemctl enable nginx
echo "<h1>Hello from $(hostname)</h1>" > /var/www/html/index.html
```

```bash
# Check if user data ran
cat /var/log/cloud-init-output.log
```

---

## EC2 Metadata Service

Every EC2 can query its own metadata at a special IP:

```bash
# Instance ID
curl http://169.254.169.254/latest/meta-data/instance-id

# Public IP
curl http://169.254.169.254/latest/meta-data/public-ipv4

# IAM role credentials
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/

# All metadata
curl http://169.254.169.254/latest/meta-data/
```

---

# EBS (Elastic Block Store)

**Persistent block storage** for EC2. Think of it as a virtual hard drive that you attach to an EC2 instance.

```
EC2 Instance
    │
    └── /dev/xvda (root volume, 20GB, gp3)
    └── /dev/xvdb (data volume, 100GB, io2)  ← attached EBS
```

**Key properties:**

- Persists independently of EC2 lifecycle
- Can detach from one EC2 and attach to another (same AZ)
- Supports snapshots (backup to S3)
- Encrypted at rest (AES-256)

---

## EBS Volume Types

|Type|IOPS|Throughput|Use Case|
|---|---|---|---|
|gp3 (SSD)|3000–16000|125–1000 MB/s|General purpose ✅ default|
|gp2 (SSD)|100–16000|128–250 MB/s|Older default|
|io2 Block Express|Up to 256,000|4000 MB/s|Critical databases|
|io1 (SSD)|Up to 64,000|1000 MB/s|High IOPS DBs|
|st1 (HDD)|500|500 MB/s|Big data, logs|
|sc1 (HDD)|250|250 MB/s|Cold storage, archival|

---

## EBS Snapshots

```bash
# Create snapshot
aws ec2 create-snapshot \
  --volume-id vol-1234567890abcdef0 \
  --description "Daily backup"

# List snapshots
aws ec2 describe-snapshots --owner-ids self

# Create volume from snapshot (restore)
aws ec2 create-volume \
  --snapshot-id snap-1234567890abcdef0 \
  --availability-zone ap-south-1a

# Copy snapshot to another region (for DR)
aws ec2 copy-snapshot \
  --source-region us-east-1 \
  --source-snapshot-id snap-1234 \
  --region ap-south-1
```

---

## Add New EBS Volume to EC2

```bash
# 1. Attach via console or CLI, then on the EC2:

# 2. Check new disk
lsblk

# 3. Format
mkfs.ext4 /dev/xvdb

# 4. Mount
mkdir /data
mount /dev/xvdb /data

# 5. Persist across reboots (/etc/fstab)
echo "/dev/xvdb /data ext4 defaults,nofail 0 2" >> /etc/fstab
```

---

# S3 (Simple Storage Service)

S3 is **object storage** — store any file, any size, accessible via HTTP. Not a filesystem. Not a database. Objects.

```
S3 Bucket: my-company-assets
├── images/logo.png           ← object
├── videos/intro.mp4          ← object
├── backups/db-2024-01-01.sql ← object
└── static/index.html         ← object
```

**Key facts:**

- Unlimited storage
- Max object size: 5TB
- 11 nines of durability (99.999999999%)
- Global namespace — bucket names must be unique worldwide
- Objects accessed via URL: `https://bucket.s3.amazonaws.com/key`

---

## S3 Storage Classes

|Class|Retrieval|Min Duration|Cost|Use|
|---|---|---|---|---|
|Standard|Instant|None|$$$|Frequent access|
|Intelligent-Tiering|Instant|None|$$$|Unknown access pattern|
|Standard-IA|Instant|30 days|$$|Infrequent access|
|One Zone-IA|Instant|30 days|$|Infrequent, non-critical|
|Glacier Instant|Instant|90 days|$|Rarely accessed|
|Glacier Flexible|Minutes–hours|90 days|$|Archive|
|Glacier Deep Archive|Hours|180 days|💲|Long-term archive|

---

## S3 Lifecycle Policies

Automatically move objects between storage classes:

```json
{
  "Rules": [{
    "Status": "Enabled",
    "Transitions": [
      { "Days": 30, "StorageClass": "STANDARD_IA" },
      { "Days": 90, "StorageClass": "GLACIER" },
      { "Days": 365, "StorageClass": "DEEP_ARCHIVE" }
    ],
    "Expiration": { "Days": 1825 }
  }]
}
```

---

## S3 Key Features

```bash
# Versioning — keeps history of every object version
aws s3api put-bucket-versioning \
  --bucket my-bucket \
  --versioning-configuration Status=Enabled

# List versions
aws s3api list-object-versions --bucket my-bucket

# Static website hosting
aws s3 website s3://my-bucket/ \
  --index-document index.html \
  --error-document error.html

# Sync local dir to S3
aws s3 sync ./dist s3://my-bucket/

# Copy with storage class
aws s3 cp backup.tar.gz s3://my-bucket/ \
  --storage-class GLACIER
```

---

## S3 Security

```bash
# Block all public access (default, recommended)
aws s3api put-public-access-block \
  --bucket my-bucket \
  --public-access-block-configuration \
    "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

# Bucket policy — allow public read (for static site)
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::my-bucket/*"
  }]
}

# Enable server-side encryption (SSE-S3)
aws s3api put-bucket-encryption \
  --bucket my-bucket \
  --server-side-encryption-configuration \
    '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'
```

---

## S3 Event Notifications

Trigger Lambda/SQS/SNS on object events:

```
Upload file to S3
    ↓
S3 Event Notification
    ↓
Lambda Function (resize image / process data)
```

---

# VPC (Virtual Private Cloud)

A **VPC** is your private, isolated network inside AWS. Think of it as your own data center network in the cloud.

---

## VPC Architecture

```
VPC: 10.0.0.0/16 (65,536 IPs)
├── Public Subnet 10.0.1.0/24 (ap-south-1a)
│   ├── EC2: Web Server
│   └── NAT Gateway
├── Public Subnet 10.0.2.0/24 (ap-south-1b)
│   └── EC2: Web Server
├── Private Subnet 10.0.3.0/24 (ap-south-1a)
│   └── EC2: App Server
├── Private Subnet 10.0.4.0/24 (ap-south-1b)
│   └── EC2: App Server
├── Private Subnet 10.0.5.0/24 (ap-south-1a)
│   └── RDS Primary
└── Private Subnet 10.0.6.0/24 (ap-south-1b)
    └── RDS Standby
│
├── Internet Gateway (public internet access)
├── Route Tables
├── Security Groups
└── NACLs
```

---

## VPC Components Deep Dive

### Internet Gateway (IGW)

- Allows public subnets to reach internet
- Attached to VPC (one per VPC)
- Route: `0.0.0.0/0 → IGW`

### NAT Gateway

- Allows **private** subnets to initiate outbound internet (updates, API calls)
- Blocks inbound connections from internet
- Lives in public subnet, paid per hour + data
- Route (private subnet): `0.0.0.0/0 → NAT Gateway`

```
Private EC2 (no public IP)
    ↓
NAT Gateway (in public subnet)
    ↓
Internet Gateway
    ↓
Internet
```

### Route Tables

```
Public Subnet Route Table:
  10.0.0.0/16  → local
  0.0.0.0/0    → igw-xxxxxxxx

Private Subnet Route Table:
  10.0.0.0/16  → local
  0.0.0.0/0    → nat-xxxxxxxx
```

### VPC Peering

- Connect two VPCs (same or different accounts/regions)
- Traffic stays in AWS backbone (not internet)
- Not transitive (A→B, B→C does NOT mean A→C)

### VPC Endpoints

- Access AWS services **without going through internet**

```
EC2 (private subnet)
    ↓ (VPC Endpoint — no NAT needed)
S3 / DynamoDB / SQS / SSM
```

```bash
# Gateway endpoint for S3
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-1234 \
  --service-name com.amazonaws.ap-south-1.s3 \
  --route-table-ids rtb-1234
```

---

# Security Groups vs NACL

|Feature|Security Group|NACL|
|---|---|---|
|Level|Instance/ENI|Subnet|
|State|Stateful|Stateless|
|Rules|Allow only|Allow + Deny|
|Evaluation|All rules evaluated|Rules in number order|
|Default|All inbound blocked|All allowed|
|Return traffic|Auto-allowed|Must explicitly allow|

---

## Security Group — Stateful

```
Inbound rule: Allow port 80 from 0.0.0.0/0
→ Response traffic automatically allowed out

Outbound rules:
  Allow all (default)
```

```bash
# Create security group
aws ec2 create-security-group \
  --group-name web-sg \
  --description "Web server SG" \
  --vpc-id vpc-1234

# Add inbound rule (allow HTTP)
aws ec2 authorize-security-group-ingress \
  --group-id sg-1234 \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0

# Allow SSH only from your IP
aws ec2 authorize-security-group-ingress \
  --group-id sg-1234 \
  --protocol tcp \
  --port 22 \
  --cidr YOUR_IP/32
```

---

## NACL — Stateless

```
Rule 100: Allow 80 inbound  → traffic comes in
Rule 200: Allow 443 inbound
Rule *  : Deny all

Response traffic — you must ALSO allow outbound:
Rule 100: Allow 1024-65535 outbound (ephemeral ports)
Rule *  : Deny all
```

---

## Security Group Chaining (Best Practice)

```
Internet → ALB-SG (port 80/443)
ALB-SG  → EC2-SG (port 8080, source: ALB-SG)
EC2-SG  → RDS-SG (port 3306, source: EC2-SG)
```

No hardcoded IPs. Source = another security group ID.

---

# Route 53

AWS's managed **DNS service** and domain registrar.

---

## Record Types

|Record|Purpose|Example|
|---|---|---|
|A|Hostname → IPv4|`app.example.com → 1.2.3.4`|
|AAAA|Hostname → IPv6||
|CNAME|Hostname → hostname|`www → app.example.com`|
|Alias|AWS resource|`app.example.com → ALB DNS`|
|MX|Mail servers||
|TXT|Verification, SPF, DKIM||
|NS|Name servers||
|SOA|Start of authority||

**Alias vs CNAME:**

- CNAME can't be at root domain (`example.com`) — use Alias
- Alias is free (no charge per query for AWS resources)
- Alias works with ALB, CloudFront, S3, API Gateway

---

## Routing Policies

|Policy|How It Works|Use Case|
|---|---|---|
|Simple|Returns one record|Single server|
|Weighted|% split across records|A/B testing, blue-green|
|Latency|Routes to lowest latency region|Global apps|
|Failover|Primary → Secondary on health fail|DR setup|
|Geolocation|Routes based on user country/continent|Legal compliance, localization|
|Geoproximity|Routes based on bias + location|Fine-grained routing|
|Multi-value|Returns multiple healthy records|Basic load balancing|

---

## Health Checks

```
Route 53 Health Check → pings your endpoint every 30s
    ↓ (if fails 3 checks)
Marks resource unhealthy
    ↓
Failover routing kicks in → traffic to backup
```

---

# Load Balancers

A **Load Balancer** distributes incoming traffic across multiple targets (EC2, containers, IPs, Lambda).

---

## Types of Load Balancers

|Type|Layer|Protocol|Use Case|
|---|---|---|---|
|ALB (Application)|L7|HTTP/HTTPS/WebSocket|Web apps, microservices|
|NLB (Network)|L4|TCP/UDP/TLS|Low latency, gaming, IoT|
|GWLB (Gateway)|L3|IP|Security appliances, firewalls|
|CLB (Classic)|L4/L7|Old|Legacy — don't use|

---

## ALB Deep Dive

```
Client
  ↓
ALB (port 443, HTTPS)
  ↓ (listener rules)
Rule 1: /api/* → Target Group: API servers (port 8080)
Rule 2: /images/* → Target Group: Image servers (port 8081)
Rule 3: default → Target Group: Web servers (port 80)
```

**ALB Features:**

- Path-based routing (`/api/*`, `/admin/*`)
- Host-based routing (`api.example.com` vs `app.example.com`)
- Header/query string routing
- SSL termination (free ACM certificate)
- Sticky sessions
- WebSocket support
- Lambda targets

```bash
# Create target group
aws elbv2 create-target-group \
  --name web-tg \
  --protocol HTTP \
  --port 80 \
  --vpc-id vpc-1234 \
  --health-check-path /health

# Register targets
aws elbv2 register-targets \
  --target-group-arn arn:aws:elasticloadbalancing:... \
  --targets Id=i-1234 Id=i-5678

# Create ALB
aws elbv2 create-load-balancer \
  --name web-alb \
  --subnets subnet-1234 subnet-5678 \
  --security-groups sg-1234
```

---

## Health Checks

```
ALB sends GET /health → target every 30s
    ↓ HTTP 200 → healthy, receives traffic
    ↓ HTTP 5xx / timeout → unhealthy, removed from rotation
    ↓ (recovers) → added back automatically
```

---

# Auto Scaling

**Auto Scaling Groups (ASG)** automatically add or remove EC2 instances based on demand.

---

## ASG Components

```
Launch Template (what to launch)
    ↓
Auto Scaling Group (how many, where)
├── Min: 2
├── Desired: 4
└── Max: 10
    ↓
Scaling Policies (when to scale)
```

---

## Scaling Policies

|Policy|How|Use Case|
|---|---|---|
|Target Tracking|Maintain metric at target (e.g. CPU 50%)|Most common ✅|
|Step Scaling|Add X instances when metric crosses threshold|Fine control|
|Scheduled|Scale at specific time|Known traffic patterns|
|Predictive|ML-based forecast|Variable recurring load|

```
Target Tracking — CPU at 50%:
  CPU hits 70% → ASG adds instances until CPU ≈ 50%
  CPU drops to 20% → ASG removes instances until CPU ≈ 50%
```

---

## ASG Lifecycle Hooks

```
Instance Launching
    ↓
Lifecycle Hook: Wait (do custom actions)
    ├── Bootstrap app
    ├── Register with config service
    └── Run tests
    ↓
InService (receives traffic)
    ↓
Scale-in triggered
    ↓
Lifecycle Hook: Wait (draining)
    ├── Complete in-flight requests
    └── Deregister from service mesh
    ↓
Terminated
```

---

# RDS (Relational Database Service)

**Managed relational database** — AWS handles provisioning, patching, backups, replication.

---

## Supported Engines

|Engine|AWS Managed|Notes|
|---|---|---|
|MySQL|✅|Most common|
|PostgreSQL|✅|Feature-rich|
|MariaDB|✅|MySQL fork|
|Oracle|✅|Licensing cost|
|SQL Server|✅|Windows workloads|
|Aurora MySQL|✅|5x MySQL performance|
|Aurora PostgreSQL|✅|3x PostgreSQL performance|

---

## RDS vs Aurora

|Feature|RDS|Aurora|
|---|---|---|
|Storage|Fixed provisioned|Auto-grows to 128TB|
|Replicas|Up to 5|Up to 15|
|Failover|1–2 min|< 30 seconds|
|Backtrack|❌|✅ (rewind DB)|
|Cost|Lower|Higher (~20% more)|
|Serverless|❌|✅ (Aurora Serverless v2)|

---

## RDS Multi-AZ vs Read Replicas

```
Multi-AZ (for HA / failover):
  Primary DB (ap-south-1a) ──sync──► Standby (ap-south-1b)
  Standby is NOT readable — only for failover
  Automatic failover in 1–2 min if primary fails

Read Replicas (for read scaling):
  Primary DB ──async──► Read Replica 1
                    └──► Read Replica 2
  App routes reads to replicas, writes to primary
  Can be in different region (cross-region replication)
```

---

## RDS Backups

```bash
# Automated backups (1–35 day retention)
# Configured in parameter groups and console

# Manual snapshot
aws rds create-db-snapshot \
  --db-instance-identifier mydb \
  --db-snapshot-identifier mydb-snapshot-2024

# Restore from snapshot
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier mydb-restored \
  --db-snapshot-identifier mydb-snapshot-2024
```

---

## RDS Security

```
VPC (private subnet only — never public)
    ↓
Security Group: only allow port 3306 from App SG
    ↓
Encryption at rest: KMS
    ↓
Encryption in transit: SSL/TLS
    ↓
Secrets Manager: store DB credentials (not hardcoded)
```

---

# ElastiCache

**Managed in-memory caching** (Redis or Memcached). Dramatically speeds up applications by caching frequent queries.

```
Without cache:
App → RDS query (100ms)

With cache:
App → ElastiCache hit (< 1ms)  ← 100x faster
App → (cache miss) → RDS → store in cache → return
```

|Feature|Redis|Memcached|
|---|---|---|
|Data structures|Rich (lists, sets, hashes)|Simple key-value|
|Persistence|✅|❌|
|Replication|✅|❌|
|Multi-AZ|✅|❌|
|Pub/Sub|✅|❌|
|Best for|Sessions, leaderboards, queues|Simple caching|

---

# CloudWatch

**Monitoring and observability** for AWS resources and applications.

---

## CloudWatch Components

|Component|What It Does|
|---|---|
|Metrics|Numeric data points over time (CPU, RAM, requests)|
|Logs|Store and search log data|
|Alarms|Alert when metric crosses threshold|
|Dashboards|Visual graphs of metrics|
|Events / EventBridge|React to AWS events|
|Container Insights|ECS/EKS metrics|
|Application Insights|App performance|

---

## Key Metrics by Service

**EC2:**

```
CPUUtilization         → CPU %
NetworkIn/Out          → bytes in/out
DiskReadOps/WriteOps   → IOPS
StatusCheckFailed      → instance or system check failed
```

**ALB:**

```
RequestCount           → requests per second
TargetResponseTime     → latency
HTTPCode_ELB_5XX       → ALB errors
HTTPCode_Target_5XX    → app errors
HealthyHostCount       → healthy targets
```

**RDS:**

```
CPUUtilization
FreeStorageSpace
DatabaseConnections
ReadLatency / WriteLatency
FreeableMemory
```

---

## CloudWatch Alarms

```bash
# Create CPU alarm
aws cloudwatch put-metric-alarm \
  --alarm-name "high-cpu" \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=InstanceId,Value=i-1234 \
  --evaluation-periods 2 \
  --alarm-actions arn:aws:sns:ap-south-1:123:my-topic

# States: OK | ALARM | INSUFFICIENT_DATA
```

---

## CloudWatch Logs

```bash
# Create log group
aws logs create-log-group --log-group-name /myapp/production

# Set retention
aws logs put-retention-policy \
  --log-group-name /myapp/production \
  --retention-in-days 30

# Query logs with Insights
aws logs start-query \
  --log-group-name /myapp/production \
  --start-time $(date -d '1 hour ago' +%s) \
  --end-time $(date +%s) \
  --query-string 'fields @timestamp, @message | filter @message like /ERROR/ | sort @timestamp desc | limit 20'
```

---

## CloudWatch Agent (for EC2 RAM metrics)

EC2 doesn't send RAM to CloudWatch by default. Install the agent:

```bash
# Install agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
dpkg -i amazon-cloudwatch-agent.deb

# Configure
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard

# Start
systemctl start amazon-cloudwatch-agent
```

---

# CloudTrail

**Audit log of every API call** in your AWS account. Who did what, when, from where.

```
IAM User loki
    ↓ runs: aws ec2 terminate-instances --instance-ids i-1234
    ↓
CloudTrail records:
  {
    "eventTime": "2024-01-15T10:30:00Z",
    "eventName": "TerminateInstances",
    "userIdentity": { "userName": "loki" },
    "sourceIPAddress": "203.0.113.5",
    "requestParameters": { "instancesSet": ["i-1234"] }
  }
```

```bash
# Look up events for a specific resource
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=ResourceName,AttributeValue=i-1234 \
  --start-time 2024-01-15T00:00:00Z

# Find who deleted an S3 bucket
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=DeleteBucket
```

---

# AWS CLI

---

## Setup

```bash
# Install
pip install awscli

# Configure (access key + secret)
aws configure

# Or use named profiles
aws configure --profile prod
aws configure --profile dev

# Use specific profile
aws s3 ls --profile prod
export AWS_PROFILE=prod
```

---

## Query with --query (JMESPath)

```bash
# Get only running instances
aws ec2 describe-instances \
  --filters Name=instance-state-name,Values=running \
  --query 'Reservations[*].Instances[*].[InstanceId,PublicIpAddress,Tags[?Key==`Name`].Value|[0]]' \
  --output table

# Get S3 bucket names only
aws s3api list-buckets --query 'Buckets[*].Name' --output text

# Get RDS endpoint
aws rds describe-db-instances \
  --db-instance-identifier mydb \
  --query 'DBInstances[0].Endpoint.Address' \
  --output text
```

---

## Common CLI Commands

```bash
# EC2
aws ec2 describe-instances
aws ec2 describe-security-groups
aws ec2 describe-vpcs
aws ec2 describe-subnets

# S3
aws s3 ls
aws s3 ls s3://my-bucket/ --recursive
aws s3 cp file.txt s3://my-bucket/
aws s3 sync ./dist s3://my-bucket/
aws s3 rm s3://my-bucket/file.txt
aws s3 presign s3://my-bucket/file.txt --expires-in 3600

# IAM
aws iam list-users
aws iam list-roles
aws iam get-user --user-name loki
aws iam list-attached-user-policies --user-name loki

# CloudWatch
aws cloudwatch list-metrics --namespace AWS/EC2
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-1234 \
  --start-time 2024-01-15T00:00:00Z \
  --end-time 2024-01-15T23:59:00Z \
  --period 3600 \
  --statistics Average
```

---

# Infrastructure as Code

**Never click through the console in production.** Use code so your infrastructure is:

- Reproducible
- Version-controlled
- Reviewable (PRs)
- Testable

---

## Terraform on AWS

```hcl
# provider.tf
provider "aws" {
  region = "ap-south-1"
}

# vpc.tf
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  tags = { Name = "main-vpc" }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "ap-south-1a"
  map_public_ip_on_launch = true
  tags = { Name = "public-subnet" }
}

# ec2.tf
resource "aws_instance" "web" {
  ami                    = "ami-0f58b397bc5c1f2e8"
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.web.id]
  key_name               = "my-key"
  user_data              = file("userdata.sh")

  tags = { Name = "web-server" }
}

# outputs.tf
output "ec2_public_ip" {
  value = aws_instance.web.public_ip
}
```

```bash
terraform init        # Initialize
terraform plan        # Preview changes
terraform apply       # Apply changes
terraform destroy     # Destroy infra
terraform state list  # View state
```

---

## CloudFormation

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Simple EC2 with Security Group

Parameters:
  InstanceType:
    Type: String
    Default: t3.micro

Resources:
  WebSG:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Web server SG
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0

  WebServer:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-0f58b397bc5c1f2e8
      InstanceType: !Ref InstanceType
      SecurityGroupIds:
        - !Ref WebSG
      Tags:
        - Key: Name
          Value: WebServer

Outputs:
  PublicIP:
    Value: !GetAtt WebServer.PublicIp
```

---

# Containers on AWS

---

## ECR (Elastic Container Registry)

**Private Docker registry** managed by AWS.

```bash
# Authenticate Docker to ECR
aws ecr get-login-password --region ap-south-1 | \
  docker login --username AWS \
  --password-stdin 123456789.dkr.ecr.ap-south-1.amazonaws.com

# Create repo
aws ecr create-repository --repository-name myapp

# Build, tag, push
docker build -t myapp .
docker tag myapp:latest 123456789.dkr.ecr.ap-south-1.amazonaws.com/myapp:latest
docker push 123456789.dkr.ecr.ap-south-1.amazonaws.com/myapp:latest
```

---

## ECS (Elastic Container Service)

AWS-native container orchestration.

```
ECS Cluster
├── Service (maintains N running tasks)
│   ├── Task Definition (like a Dockerfile for your app)
│   │   ├── Container: nginx (image, ports, env, resources)
│   │   └── Container: app (image, ports, env, resources)
│   └── Tasks (running instances of task definition)
└── Capacity: EC2 or Fargate
```

**ECS vs EKS:**

||ECS|EKS|
|---|---|---|
|Type|AWS-native|Managed Kubernetes|
|Learning curve|Low|High|
|Control|Less|More|
|Ecosystem|AWS-only|CNCF/Kubernetes|
|Cost|Cheaper|More expensive|
|Use when|AWS-only shop|Need K8s|

---

## Fargate

**Serverless containers** — run containers without managing EC2 servers.

```
You define: CPU, memory, container image
AWS manages: EC2 fleet, patching, scaling

ECS + Fargate = Just run your container
EKS + Fargate = Kubernetes without node management
```

---

## EKS (Elastic Kubernetes Service)

**Managed Kubernetes control plane.**

```bash
# Create EKS cluster
eksctl create cluster \
  --name my-cluster \
  --region ap-south-1 \
  --nodegroup-name workers \
  --node-type t3.medium \
  --nodes 3

# Configure kubectl
aws eks update-kubeconfig --name my-cluster --region ap-south-1

# Verify
kubectl get nodes
kubectl get pods -A
```

---

# Serverless

---

## Lambda

**Run code without servers.** Pay per 100ms of execution.

```
Trigger
  ├── API Gateway (HTTP)
  ├── S3 Event (file upload)
  ├── SQS (message)
  ├── EventBridge (schedule / event)
  ├── DynamoDB streams
  └── CloudWatch Events
    ↓
Lambda Function (Python, Node.js, Go, Java...)
    ↓
Response / Action
```

```python
# Python Lambda handler
import json
import boto3

def handler(event, context):
    s3 = boto3.client('s3')

    # Triggered by S3 upload
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    print(f"New file: s3://{bucket}/{key}")

    return {
        'statusCode': 200,
        'body': json.dumps('Processed!')
    }
```

**Lambda limits:**

- Max execution: 15 minutes
- Max memory: 10GB
- Max package size: 250MB (unzipped)
- Max /tmp storage: 10GB

---

## API Gateway + Lambda (Serverless API)

```
Client
  ↓
API Gateway (routes, auth, rate limiting)
  ↓
Lambda Function
  ↓
DynamoDB / RDS / S3
```

---

## SQS + Lambda (Event Queue Processing)

```
App → SQS Queue → Lambda (batch processor) → DB
                ↑
           (on failure)
                ↓
         Dead Letter Queue (DLQ)
```

---

# Cost Management

---

## Cost Optimization Strategies

```
1. Right-size instances
   → t3.2xlarge for dev? Use t3.small instead

2. Use Reserved Instances for predictable workloads
   → Save 40–72% vs On-Demand

3. Spot Instances for batch/CI
   → Save up to 90%

4. S3 lifecycle policies
   → Auto-archive old objects to Glacier

5. Delete unused resources
   → Unattached EBS volumes, old snapshots, idle NAT Gateways

6. Use CloudFront
   → Reduces data transfer costs from EC2/S3

7. Savings Plans
   → Commit to $/hr spend across EC2/Lambda/Fargate
```

---

## Key Cost Culprits

|Service|Common Waste|
|---|---|
|EC2|Oversized instances left running|
|EBS|Unattached volumes|
|NAT Gateway|Data processing charges|
|RDS|Multi-AZ in dev (not needed)|
|Snapshots|Forgotten old snapshots|
|Data Transfer|Cross-region / internet egress|

```bash
# Find unattached EBS volumes
aws ec2 describe-volumes \
  --filters Name=status,Values=available \
  --query 'Volumes[*].[VolumeId,Size,CreateTime]' \
  --output table

# Find old snapshots
aws ec2 describe-snapshots --owner-ids self \
  --query 'Snapshots[*].[SnapshotId,StartTime,VolumeSize]' \
  --output table
```

---

# Security Best Practices

---

## AWS Security Checklist

```
Account Level:
  ✅ Enable root MFA (hardware key if possible)
  ✅ Never create root access keys
  ✅ Enable CloudTrail in all regions
  ✅ Enable AWS Config (compliance monitoring)
  ✅ Enable GuardDuty (threat detection)
  ✅ Set billing alerts

IAM:
  ✅ No wildcard Action: * in policies
  ✅ Use IAM roles for services (not access keys)
  ✅ MFA for all human users
  ✅ Use IAM Access Analyzer
  ✅ Rotate access keys every 90 days

Network:
  ✅ No 0.0.0.0/0 on SSH/RDP to EC2
  ✅ Use VPN or Bastion host for SSH
  ✅ Private subnets for databases
  ✅ Enable VPC Flow Logs

Data:
  ✅ Enable S3 Block Public Access (account level)
  ✅ Encrypt EBS volumes (KMS)
  ✅ Encrypt RDS at rest and in transit
  ✅ Use Secrets Manager (not hardcoded credentials)

Logging:
  ✅ CloudTrail → S3 (all regions, all services)
  ✅ VPC Flow Logs → CloudWatch
  ✅ ALB access logs → S3
```

---

## Secrets Manager vs SSM Parameter Store

||Secrets Manager|SSM Parameter Store|
|---|---|---|
|Cost|$0.40/secret/month|Free (Standard)|
|Rotation|Automatic ✅|Manual|
|DB credentials|Built-in rotation|Manual|
|Use for|DB passwords, API keys|Config values, non-secret params|

```python
# Fetch secret in Lambda/EC2
import boto3, json

client = boto3.client('secretsmanager')
secret = client.get_secret_value(SecretId='prod/myapp/db')
db_creds = json.loads(secret['SecretString'])

# db_creds['username'], db_creds['password']
```

---

# 🚑 Real-World Scenarios

---

## Scenario 1 — EC2 Instance Unreachable (Can't SSH)

### Symptoms

```
ssh: connect to host 54.x.x.x port 22: Connection timed out
```

### Investigation (in order)

```bash
# 1. Is the instance running?
aws ec2 describe-instances \
  --instance-ids i-1234 \
  --query 'Reservations[0].Instances[0].State.Name'

# 2. Does it have a public IP?
aws ec2 describe-instances \
  --instance-ids i-1234 \
  --query 'Reservations[0].Instances[0].PublicIpAddress'

# 3. Check Security Group — is port 22 allowed?
aws ec2 describe-security-groups --group-ids sg-1234

# 4. Check Status Checks in console
aws ec2 describe-instance-status --instance-ids i-1234

# 5. Check NACL — is port 22 allowed inbound + ephemeral ports outbound?
# (Console: VPC → Subnets → NACL tab)
```

### Diagnosis Decision Tree

```
Instance stopped?           → Start it
No public IP?               → Allocate and associate Elastic IP
SG blocks port 22?          → Add inbound rule: TCP 22, your IP/32
Instance status check fail? → Stop/Start (moves to new host)
System status check fail?   → AWS hardware issue, wait or migrate
NACL blocking?              → Add allow rule (and ephemeral return)
```

### Fix

```bash
# Open SSH in SG
aws ec2 authorize-security-group-ingress \
  --group-id sg-1234 \
  --protocol tcp --port 22 \
  --cidr $(curl -s ifconfig.me)/32
```

---

## Scenario 2 — Website Returns 502 Bad Gateway

### Symptoms

```
Browser: 502 Bad Gateway
ALB → Target Group → EC2 App
```

### Investigation

```bash
# 1. Check target health in ALB
aws elbv2 describe-target-health \
  --target-group-arn arn:aws:elasticloadbalancing:...

# Possible: unhealthy | draining | initial

# 2. SSH to EC2, check the app
systemctl status myapp
journalctl -u myapp -xe

# 3. Check if app is actually listening on expected port
ss -tulnp | grep :8080

# 4. Check security group — does ALB SG have access to EC2 on app port?
# ALB SG → EC2 SG port 8080

# 5. Check ALB access logs (if enabled)
aws s3 ls s3://my-alb-logs/
```

### Diagnosis

```
App crashed?                → systemctl restart myapp
App on wrong port?          → fix app config or TG port
SG blocks ALB→EC2?          → add inbound rule from ALB-SG
Health check path wrong?    → fix /health endpoint in TG config
All targets unhealthy?      → check EC2 logs, app startup errors
```

---

## Scenario 3 — S3 Upload Works But Objects Not Accessible

### Symptoms

```
Objects uploaded via app
URL returns 403 Forbidden or 404
```

### Investigation

```bash
# 1. Check bucket policy
aws s3api get-bucket-policy --bucket my-bucket

# 2. Check public access block (often the culprit)
aws s3api get-public-access-block --bucket my-bucket

# 3. Check object ACL
aws s3api get-object-acl --bucket my-bucket --key my-file.txt

# 4. Check if object actually exists
aws s3api head-object --bucket my-bucket --key my-file.txt

# 5. Check IAM permissions of the accessing user/role
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123:role/my-role \
  --action-names s3:GetObject \
  --resource-arns arn:aws:s3:::my-bucket/*
```

### Fix

```bash
# For public static website — allow public read
aws s3api put-public-access-block \
  --bucket my-bucket \
  --public-access-block-configuration \
    "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false"

# Then add bucket policy
aws s3api put-bucket-policy --bucket my-bucket --policy '{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::my-bucket/*"
  }]
}'
```

---

## Scenario 4 — RDS Connection Refused from EC2

### Symptoms

```
Can't connect to MySQL: (111) Connection refused
timeout connecting to RDS endpoint
```

### Investigation

```bash
# 1. Can EC2 reach the RDS endpoint at all?
nc -zv mydb.abcdef.ap-south-1.rds.amazonaws.com 3306

# 2. Check RDS instance status
aws rds describe-db-instances \
  --db-instance-identifier mydb \
  --query 'DBInstances[0].DBInstanceStatus'

# 3. Check RDS Security Group — does it allow port 3306 from EC2's SG?
aws ec2 describe-security-groups --group-ids sg-rds-1234

# 4. Are they in the same VPC?
aws rds describe-db-instances --db-instance-identifier mydb \
  --query 'DBInstances[0].DBSubnetGroup.VpcId'

# 5. Check DB subnet group — is RDS in correct subnet?
aws rds describe-db-subnet-groups
```

### Fix

```bash
# Add EC2's security group as source to RDS SG
aws ec2 authorize-security-group-ingress \
  --group-id sg-rds-1234 \
  --protocol tcp \
  --port 3306 \
  --source-group sg-ec2-5678

# Never expose RDS to 0.0.0.0/0
```

---

## Scenario 5 — Lambda Function Timing Out

### Symptoms

```
Task timed out after 3.00 seconds
```

### Investigation

```bash
# Check CloudWatch Logs for the function
aws logs filter-log-events \
  --log-group-name /aws/lambda/my-function \
  --filter-pattern "Task timed out"

# Check duration metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Duration \
  --dimensions Name=FunctionName,Value=my-function \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 60 \
  --statistics Maximum Average
```

### Diagnosis & Fix

```
Default timeout: 3 seconds (often too low)

Fix 1: Increase timeout (max: 15 min)
  aws lambda update-function-configuration \
    --function-name my-function \
    --timeout 60

Fix 2: Is Lambda trying to reach internet?
  → Lambda in VPC needs NAT Gateway for outbound
  → No VPC: has internet by default

Fix 3: Is it a cold start + slow DB connection?
  → Move DB connection outside handler (reuse across invocations)
  → Use RDS Proxy for connection pooling

Fix 4: External API slow?
  → Add timeout to your HTTP calls (requests.get(url, timeout=5))

Fix 5: Not enough memory (CPU scales with memory)
  → Increase memory: 128MB → 512MB (also gives more CPU)
```

---

## Scenario 6 — Auto Scaling Not Triggering

### Symptoms

```
CPU at 90% for 10 minutes
No new instances launched
```

### Investigation

```bash
# 1. Check scaling policy
aws autoscaling describe-policies \
  --auto-scaling-group-name my-asg

# 2. Check scaling activities
aws autoscaling describe-scaling-activities \
  --auto-scaling-group-name my-asg

# 3. Check CloudWatch alarm state
aws cloudwatch describe-alarms \
  --alarm-names "high-cpu-alarm"

# 4. Is ASG at max capacity?
aws autoscaling describe-auto-scaling-groups \
  --auto-scaling-group-names my-asg \
  --query 'AutoScalingGroups[0].[MinSize,DesiredCapacity,MaxSize]'
```

### Fix

```
ASG at MaxSize?        → Increase MaxSize
Alarm in INSUFFICIENT_DATA? → Check alarm dimensions match instance
Cooldown period?       → Wait (default: 300s between scale events)
Launch template error? → Check EC2 activity log for errors
AMI not found?         → Update Launch Template with valid AMI
```

---

## Scenario 7 — CloudWatch Alarm Not Triggering

### Symptoms

```
CPU is clearly high in console
Alarm stays in OK state
```

### Diagnosis

```bash
# 1. Check alarm math — is threshold correct?
aws cloudwatch describe-alarms --alarm-names my-alarm

# 2. Check metric namespace and dimension exactly
# Common mistake: namespace is AWS/EC2 but dimensions wrong
aws cloudwatch list-metrics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-1234

# 3. EC2 RAM not in CloudWatch by default
# → Install CloudWatch Agent for memory metrics

# 4. Check period vs evaluation periods
# Period: 300s, EvaluationPeriods: 2 = needs 10 min of high CPU
```

---

## 🔎 AWS Incident Response Workflow

When something breaks in production:

```
1. DETECT
   → CloudWatch alarm fires
   → Users report issues

2. TRIAGE
   → What service is affected?
   → How many users impacted?
   → When did it start?

3. INVESTIGATE
   → CloudWatch metrics (CPU, error rates, latency)
   → CloudWatch Logs (error messages)
   → CloudTrail (did anyone change something?)
   → X-Ray traces (where in the call chain?)

4. MITIGATE (buy time, don't fix root cause yet)
   → Roll back bad deployment
   → Increase capacity (ASG)
   → Route traffic away (Route53 failover)
   → Disable problematic feature flag

5. RESOLVE
   → Fix root cause
   → Test in staging first

6. POST-MORTEM
   → Write incident report
   → Timeline of events
   → Root cause
   → Action items to prevent recurrence
```

---

# Interview Questions

## Q: What is the difference between Security Group and NACL?

**Security Group:**

- Stateful: return traffic auto-allowed
- Instance/ENI level
- Allow rules only
- All rules evaluated together

**NACL:**

- Stateless: must explicitly allow return traffic
- Subnet level
- Allow + Deny rules
- Rules evaluated in number order (lowest first)

**When to use NACL:** when you need to explicitly DENY specific IPs (e.g., block an attacker's IP fast).

---

## Q: What is the difference between S3 and EBS?

**S3:** Object storage. Access via HTTP. Unlimited capacity. Not attached to EC2. Good for files, backups, static websites, data lakes.

**EBS:** Block storage. Attached to EC2 like a hard drive. AZ-specific. Good for OS, databases, file systems.

---

## Q: Difference between NAT Gateway and Internet Gateway?

**Internet Gateway:** allows resources with public IPs to communicate with the internet (both directions).

**NAT Gateway:** allows resources with only private IPs to initiate outbound connections to the internet. Blocks unsolicited inbound. Lives in public subnet.

---

## Q: What is an IAM Role vs IAM User?

**IAM User:** Long-term identity for a human. Has permanent credentials (password, access keys).

**IAM Role:** Temporary identity assumed by services, EC2s, Lambda, or even other accounts. No permanent credentials — AWS STS issues temp tokens. Best practice for any non-human access.

---

## Q: What happens when an EC2 in an ASG fails a health check?

1. ASG marks the instance unhealthy
2. ASG terminates the unhealthy instance
3. ASG launches a replacement instance
4. New instance goes through lifecycle hooks
5. Registers with Target Group, starts receiving traffic

---

## Q: Difference between ALB and NLB?

**ALB:** Layer 7. HTTP/HTTPS. Can route by path, hostname, headers. SSL termination. Good for web apps, microservices.

**NLB:** Layer 4. TCP/UDP. Ultra-low latency (~100μs). Preserves client IP. Good for gaming, IoT, financial apps. Can handle millions of requests per second.

---

## Q: What is VPC peering? What are its limitations?

VPC Peering connects two VPCs privately. Traffic stays on AWS backbone.

**Limitations:**

- Not transitive (A↔B, B↔C doesn't mean A↔C)
- No overlapping CIDR ranges
- One peering connection per pair

**Alternative:** AWS Transit Gateway (hub-and-spoke, transitive, supports 5000 VPCs).

---

## Q: What is the difference between RDS Multi-AZ and Read Replicas?

**Multi-AZ:**

- Synchronous replication to standby
- Standby is NOT readable
- Purpose: high availability / automatic failover
- Standby in different AZ

**Read Replicas:**

- Asynchronous replication
- Replicas ARE readable (offload reads)
- Purpose: scale read performance
- Can be cross-region

---

## Q: What is CloudTrail vs CloudWatch?

**CloudTrail:** WHO did WHAT in AWS. API audit log. Security, compliance, forensics.

**CloudWatch:** HOW is it performing. Metrics, logs, alarms. Monitoring, observability.

---

## Q: How would you design a highly available 3-tier architecture on AWS?

```
Route 53 (DNS + health checks)
    ↓
CloudFront (CDN + WAF)
    ↓
ALB (multi-AZ, across 2+ public subnets)
    ↓
ASG of EC2 (across 2+ private subnets) — app tier
    ↓
RDS Multi-AZ + Read Replicas (in private DB subnets)
ElastiCache (Redis, session/cache layer)

Supporting:
- VPC with public/private subnets in 2+ AZs
- NAT Gateway (per AZ for HA) in public subnets
- S3 for static assets + CloudFront
- CloudWatch + SNS for alerting
- CloudTrail for auditing
- Secrets Manager for credentials
```

---

# Practice Labs

## Lab 1 — Launch EC2 & SSH In

```bash
# Launch
aws ec2 run-instances \
  --image-id ami-0f58b397bc5c1f2e8 \
  --instance-type t3.micro \
  --key-name my-key \
  --security-group-ids sg-1234 \
  --subnet-id subnet-1234

# Get IP
aws ec2 describe-instances \
  --query 'Reservations[*].Instances[*].PublicIpAddress' \
  --output text

# SSH
ssh -i my-key.pem ubuntu@<public-ip>
```

## Lab 2 — Host Nginx + Expose via ALB

```bash
# On EC2:
sudo apt update && sudo apt install nginx -y
echo "<h1>Hello from $(hostname)</h1>" | sudo tee /var/www/html/index.html

# In AWS Console / CLI:
# 1. Create Target Group (port 80, /health check)
# 2. Register EC2 as target
# 3. Create ALB (public subnets, SG allowing port 80)
# 4. Create listener (port 80 → target group)
# 5. Access ALB DNS name
```

## Lab 3 — S3 Static Website with CloudFront

```bash
# Create bucket
aws s3 mb s3://my-static-site-unique-name

# Upload files
aws s3 sync ./dist s3://my-static-site-unique-name/

# Enable website hosting
aws s3 website s3://my-static-site-unique-name/ \
  --index-document index.html

# Create CloudFront distribution pointing to S3
# Use OAC (Origin Access Control) for security
```

## Lab 4 — VPC from Scratch

```
Create:
  1. VPC: 10.0.0.0/16
  2. Public Subnets: 10.0.1.0/24, 10.0.2.0/24
  3. Private Subnets: 10.0.3.0/24, 10.0.4.0/24
  4. Internet Gateway → attach to VPC
  5. Public Route Table: 0.0.0.0/0 → IGW
  6. NAT Gateway in public subnet
  7. Private Route Table: 0.0.0.0/0 → NAT
  8. Launch EC2 in each subnet, test connectivity
```

## Lab 5 — CloudWatch Alarm + SNS Alert

```bash
# Create SNS topic
aws sns create-topic --name alerts

# Subscribe email
aws sns subscribe \
  --topic-arn arn:aws:sns:ap-south-1:123:alerts \
  --protocol email \
  --notification-endpoint you@email.com

# Create CPU alarm → notify SNS
aws cloudwatch put-metric-alarm \
  --alarm-name high-cpu \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=InstanceId,Value=i-1234 \
  --evaluation-periods 2 \
  --alarm-actions arn:aws:sns:ap-south-1:123:alerts
```

## Lab 6 — Deploy App with Terraform

```bash
mkdir terraform-lab && cd terraform-lab

# Write main.tf with provider, VPC, EC2, SG
terraform init
terraform plan
terraform apply
terraform destroy   # clean up
```

## Lab 7 — Deploy Container on ECS Fargate

```bash
# 1. Push image to ECR
# 2. Create ECS Cluster (Fargate)
# 3. Create Task Definition (container, CPU, memory, port)
# 4. Create Service (desired count: 2, attach to ALB)
# 5. Access via ALB DNS
```

---

# Learning Roadmap

```
Phase 1 — Core Services (Week 1-2)
  ├── IAM (users, roles, policies)
  ├── EC2 (launch, SSH, SG)
  ├── S3 (upload, website, versioning)
  └── VPC (subnets, IGW, routes)

Phase 2 — Production Basics (Week 3-4)
  ├── ALB + Target Groups
  ├── Auto Scaling Groups
  ├── RDS (MySQL/PostgreSQL)
  ├── CloudWatch + Alarms
  └── Route 53

Phase 3 — DevOps & IaC (Week 5-6)
  ├── AWS CLI mastery
  ├── Terraform on AWS
  ├── CodePipeline / CodeBuild (CI/CD)
  ├── ECR + ECS/Fargate
  └── ElastiCache

Phase 4 — Advanced (Week 7-8+)
  ├── EKS (Kubernetes)
  ├── Lambda + API Gateway
  ├── CloudFront + WAF
  ├── Security (GuardDuty, Security Hub)
  ├── Cost Optimization
  └── Multi-region architecture

Certifications Path:
  Cloud Practitioner → Solutions Architect Associate
  → DevOps Engineer Professional / SysOps Administrator
```

---

# Production Architecture Reference

```
                         [Route 53]
                              │
                         [CloudFront + WAF]
                              │
                     [Application Load Balancer]
                    /          │           \
              [AZ-1a]       [AZ-1b]      [AZ-1c]
                 │              │              │
            [EC2 ASG]      [EC2 ASG]     [EC2 ASG]
                 │              │              │
            [ElastiCache Redis Cluster]
                 │
        [RDS Aurora Multi-AZ]
       Primary          Replica

Supporting Services:
  S3 (assets, backups, logs)
  ECR (container images)
  Secrets Manager (credentials)
  CloudWatch (metrics + logs + alarms)
  CloudTrail (audit)
  SNS (alerting)
  SQS (async processing)
```

---

_Last updated: 2025 | Build it. Break it. Fix it. 🚀_