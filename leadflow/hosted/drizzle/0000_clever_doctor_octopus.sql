CREATE TABLE `events` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`session` text NOT NULL,
	`lead_id` integer NOT NULL,
	`description` text NOT NULL,
	`created` text NOT NULL
);
--> statement-breakpoint
CREATE TABLE `leads` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`session` text NOT NULL,
	`name` text NOT NULL,
	`email` text NOT NULL,
	`company` text NOT NULL,
	`budget` integer NOT NULL,
	`message` text NOT NULL,
	`score` integer NOT NULL,
	`stage` text DEFAULT 'New' NOT NULL,
	`followup` text DEFAULT '' NOT NULL,
	`created` text NOT NULL
);
--> statement-breakpoint
CREATE UNIQUE INDEX `session_email` ON `leads` (`session`,`email`);