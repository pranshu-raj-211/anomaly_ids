# anomaly_ids

A rule based intrusion detection system (IDS) that works on the basis of statistical models based on usage patterns of particular users.

Basically a script collects data on your usage patterns while you use your system as usual, statistical patterns are found according to that and used to detect anomalies in system usage, specifically for things like memory utilization, network io, disk io etc.

It might be evident that this works on the premise of the user's data, as the system metrics would differ a lot based on the operating system, system specs and installed software (for instance, linux based systems have a memory utilization which is much lesser than that of windows).

In the future, I'd like to extend this by adding more rules, as well as support for port scanning and a good algorithm to find the anomalies with less data.
