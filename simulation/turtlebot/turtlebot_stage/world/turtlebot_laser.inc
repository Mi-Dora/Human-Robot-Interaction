
define hokuyolaser ranger
(
	sensor
	( 			
		# laser-specific properties
		# factory settings for LMS200	
		range [ 0.0  30.0 ]
		fov 180.0
		samples 721
	)

	# generic model properties
	color "blue"
	size [ 0.05 0.06 0.05 ] # dimensions from LMS200 data sheet	
)


define turtlebot position
(
  pose [ 0.0 0.0 0.0 0.0 ]

  odom_error [0.03 0.03 999999 999999 999999 0.02]

  size [ 0.2552 0.2552 0.40 ]
  origin [ 0.0 0.0 0.0 0.0 ]
  gui_nose 1
  drive "diff"
  color "gray"
  
  hokuyolaser( pose [-0.005 0.00 -0.03 0 ])

)
