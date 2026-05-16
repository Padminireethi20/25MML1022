# Campus Notification System Design

---

# Stage 1 — REST API Design

## Objective

Design REST APIs for a campus notification system supporting:
- notification delivery
- read/unread tracking
- deletion
- real-time updates

---

## APIs

### 1. Get Notifications

GET /api//notifications/{studentId}

### Response

```json
{
  "notifications": [
    {
      "id": 1,
      "type": "Placement",
      "message": "Google Hiring",
      "isRead": false
    }
  ]
}
```

---

### 2. Send Notification

POST /api/notifications

### Request

```json
{
  "studentId": 102,
  "type": "Placement",
  "message": "Amazon Hiring"
}
```

---

### 3. Mark Notification Read

PATCH /api/notifications/{id}/read

---

### 4. Delete Notification

DELETE /api/notifications/{id}

---

## Real-Time Notification Delivery

Use WebSockets for real-time communication.

Advantages:
- low latency
- instant updates
- reduced polling overhead

For scalability:
- Redis Pub/Sub can distribute messages across multiple servers.

---

# Stage 2 — Database Design

## Database Choice

Use PostgreSQL because:
- structured relational data
- ACID compliance
- indexing support
- efficient filtering and sorting

---

## Notifications Table

| Column | Type |
|---|---|
| id | UUID |
| student_id | VARCHAR |
| type | VARCHAR |
| message | TEXT |
| is_read | BOOLEAN |
| created_at | TIMESTAMP |

---

## Scaling Challenges

Challenges:
- millions of notifications
- high concurrent reads
- slow filtering queries

Solutions:
- indexing
- table partitioning
- replication
- Redis caching

---

# Stage 3 — Query Optimization

## Problem

Fetching unread notifications becomes slow for large datasets due to full table scans.Knapsack can be used to optimise the logic

---

## Solution

Create composite index:

```sql
CREATE INDEX idx_notifications_student_read_created
ON notifications(student_id, is_read, created_at DESC);
```

---

## Why Not Index Every Column?

Indexing every column:
- increases storage usage
- slows write operations
- increases maintenance overhead

Indexes should only be created for frequently queried fields.

---

# Stage 4 — Performance Optimization

## Optimizations

### 1. Redis Caching

Cache frequently accessed notifications.

---

### 2. Pagination

Load notifications page by page instead of all at once.

---

### 3. Lazy Loading

Load additional notifications only when needed.

---

### 4. WebSocket Push

Avoid continuous polling by pushing updates in real-time.

---

# Stage 5 — Large Scale Notification Architecture

## Problems in Existing System

- sequential notification processing
- blocking API calls
- no retry mechanism
- slow delivery during high traffic

---

## Improved Architecture

Use:
- Kafka or RabbitMQ
- asynchronous workers
- retry mechanism
- dead letter queue
- batch processing

---

## Benefits

- scalable
- fault tolerant
- high throughput
- non-blocking processing

---

# Stage 6 — Priority Inbox Implementation

## Objective

Prioritize notifications based on:
1. Placement
2. Results
3. Events

Then sort by most recent notifications.

---

## Approach

Use:
- priority mapping
- sorting
- priority queue / heap

---

## Priority Mapping

| Type | Priority |
|---|---|
| Placement | 1 |
| Results | 2 |
| Event | 3 |

---

## Final Behavior

Return:
- highest priority notifications
- most recent first
- top 10 notifications