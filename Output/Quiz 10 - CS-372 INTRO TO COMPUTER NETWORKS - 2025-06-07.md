Quiz 10 - CS-372 INTRO TO COMPUTER NETWORKS - 2025-06-07
----------------------------------------
# Quiz 10 - CS-372 INTRO TO COMPUTER NETWORKS - 2025-06-07

**Total Score:** 38.5/45.0 pts

----------------------------------------
**Question 1: ◯ PARTIAL CREDIT - 0.5/2.0 pts**

Which of the following are used in a wireless network such as 802.11n?



- ⌕ Selected Possibly: Option 1: Exponential back-off/retry for collision resolution

- Option 2: Collision Avoidance

- Option 3: Reservation system with Request to Send (RTS) and Clear to Send (CTS)

- Option 4: Collision Detection

- Option 5: Carrier Sense Multiple Access



---

----------------------------------------
**Question 2: ✓ CORRECT - 2.0/2.0 pts**

In direct routing, after the initial contact with the home network, the correspondent sends packets to



- ✓ Selected Correct: Option 1: The care-of address



---

----------------------------------------
**Question 3: ✓ CORRECT - 2.0/2.0 pts**

The default multiple access scheme of 802.11g is RTS/CTS.



- ✓ Selected Correct: Option 1: False



---

----------------------------------------
**Question 4: ✓ CORRECT - 2.0/2.0 pts**

A device which moves between networks is a Mobile device.



- ✓ Selected Correct: Option 1: Mobile



---

----------------------------------------
**Question 5: ✓ CORRECT - 2.0/2.0 pts**

In one type of wireless network, hosts communicate directly with other hosts that are within range. This communication model forms a "grid" called a(n)



- ✓ Selected Correct: Option 1: ad-hoc network



---

----------------------------------------
**Question 6: ✓ CORRECT - 2.0/2.0 pts**

A device which is connected to the network through a link which does not utilize any physical connection is a Wireless device.



- ✓ Selected Correct: Option 1: Wireless



---

----------------------------------------
**Question 7: ✓ CORRECT - 2.0/2.0 pts**

In one type of wireless network, hosts communicate through a central “base station” access point, which is typically connected to a wired network. This communication model is called a(n)



- ✓ Selected Correct: Option 1: infrastructure network



---

----------------------------------------
**Question 8: ✓ CORRECT - 2.0/2.0 pts**

When a mobile unit moves from a home or foreign agent to another (foreign) agent, the new agent must assign.... (Check all that apply)



- ✓ Selected Correct: Option 1: a new “care-of” address to the mobile unit



---

----------------------------------------
**Question 9: ✓ CORRECT - 2.0/2.0 pts**

Which of the following are major issues that must be handled in wireless networks (i.e., issues that are more significant than in wired networks). Check all that apply.



- ✓ Selected Correct: Option 1: Radio waves are more susceptible to interference than signals carried on cable

- ✓ Selected Correct: Option 2: The "hidden node" problem

- ✓ Selected Correct: Option 3: Hosts may frequently move from one network to another

- ✓ Selected Correct: Option 4: Multi-path propagation when radio signals bounce off obstacles

- ✓ Selected Correct: Option 5: Obstacles that block radio signals



---

----------------------------------------
**Question 10: ✕ INCORRECT - 0.0/2.0 pts**

In indirect routing, after the initial contact with the home network, the correspondent sends packets to



- Option 1: The care-of address

- ✕ Selected Incorrect: Option 2: The foreign agent

- Option 3: The permanent address



---

----------------------------------------
**Question 11: ✓ CORRECT - 2.0/2.0 pts**

In one type of wireless network, hosts communicate directly with other hosts that are within range. This communication model forms a "grid" called a(n)



- ✓ Selected Correct: Option 1: ad-hoc network



---

----------------------------------------
**Question 12: ✓ CORRECT - 2.0/2.0 pts**

Which of the following are used in a wireless network such as 802.11n?



- ✓ Selected Correct: Option 1: Exponential back-off/retry for collision resolution

- ✓ Selected Correct: Option 2: Carrier Sense Multiple Access

- ✓ Selected Correct: Option 3: Reservation system with Request to Send (RTS) and Clear to Send (CTS)

- ✓ Selected Correct: Option 4: Collision Avoidance



---

----------------------------------------
**Question 13: ✓ CORRECT - 4.0/4.0 pts**

S represents a source host and D represents a destination host . Which of the following is the most typical use of public key encryption, when S sends an authenticated (digitally signed) message to D ?



- ✓ Selected Correct: Option 1: S encrypts a signature using S's private key, and D decrypts the signature using S's public key.



---

----------------------------------------
**Question 14: ✓ CORRECT - 4.0/4.0 pts**

Given an encryption scheme that uses encrypt(m) to encrypt message m , and uses decrypt(c) to get back the original message. ( m is the original message, and c is the encrypted message.) Which of the following must be true?



- ✓ Selected Correct: Option 1: decrypt(encrypt(m)) = m



---

----------------------------------------
**Question 15: ✓ CORRECT - 4.0/4.0 pts**

When using an RSA algorithm to construct private and public keys for a public key encryption system, choose prime numbers p and q , and then calculate n = pq , z = (p-1)(q-1) . Then choose e and d to create the public key and the private key . Suppose that p = 5 , and q = 11 . Which of the following values will work for d and e ? Check all that apply.



- ✓ Selected Correct: Option 1: e = 7, d = 63



---

----------------------------------------
**Question 16: ✓ CORRECT - 3.0/3.0 pts**





![Image](./Matthew Baker's Quiz History_ Module 10 Summary Exercises_files/overlapping_802.11_nets.jpg)

Suppose now that A sends messages to B, and D sends messages to C. What is the combined maximum rate at which data messages can flow from A to B and from D to C?



- ✓ Selected Correct: Option 1: 2 messages/slot.



---

----------------------------------------
**Question 17: ✕ INCORRECT - 0.0/3.0 pts**





![Image](./Matthew Baker's Quiz History_ Module 10 Summary Exercises_files/overlapping_802.11_nets.jpg)

Suppose now that A sends messages to B, and C sends messages to D. What is the combined maximum rate at which data messages can flow from A to B and from C to D?



- Option 1: 0.25 messages/slot (i.e., one message every four slots).

- Option 2: 0.5 messages/slot (i.e., 1 message every two slots).

- Option 3: 1 message/slot.

- ✕ Selected Incorrect: Option 4: 2 messages/slot.



---

----------------------------------------
**Question 18: ✓ CORRECT - 3.0/3.0 pts**



Consider the scenario shown below in which there are four wireless nodes, A, B, C, and D. The radio coverage of the four nodes is shown via the shaded ovals; all nodes share the same frequency. When A transmits, it can only be heard/received by B; when B transmits, both A and C can hear/receive from B; when C transmits, both B and D can hear/receive from C; when D transmits, only C can hear/receive from D. If a node hears two simultaneous transmissions at a time, the messages interfere at that receiver, even through they may not interfere at other receivers, where only one of the messages is heard.[ Make sure you understand this paragraph. ]

Suppose now that each node has an infinite supply of messages that it wants to send to each of the other nodes. If a message’s destination is not an immediate neighbor, then the message must be relayed. For example, if A wants to send to D, a message from A must first be sent to B, which then sends the message to C, which then sends the message to D. Time is slotted, with a message transmission time taking exactly one time slot, e.g., as in slotted Aloha. During a slot, a node can do one of the following: (i) send a message (ii) receive a message (if exactly one message is being sent to it), (iii) remain silent. As always, if a node hears two or more simultaneous transmissions, a collision occurs and none of the transmitted messages are received successfully.

You can assume here that there are no bit-level errors, and thus if exactly one message is heard at a receiver, it will be received correctly at that receiver.



![Image](./Matthew Baker's Quiz History_ Module 10 Summary Exercises_files/overlapping_802.11_nets.jpg)

Suppose now that an omniscient controller (e.g., a controller that knows the state of every node in the network) can command each node to do whatever it (the omniscient controller) wishes, that is, to send a message, to receive a message, or to remain silent. Given this omniscient controller, what is the maximum rate at which messages can be transferred from C to A, given that there are no other messages between any other source/destination pairs?



- ✓ Selected Correct: Option 1: 0.5 messages/slot (i.e., 1 message every two slots).



---

