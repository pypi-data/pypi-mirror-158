# Change Log

<!--next-version-placeholder-->

## v0.1.2.dev8 (13/07/2022)

- bug fix in `_FunctionWrapper`, for functions with extra arguments like
  `BaseProblem.hessian_times_vector(m, v)` and `BaseProblem.jacobian_times_vector(m, v)`

## v0.1.2.dev7 (15/06/2022)

- bug fix in `BaseSolver.model_covariance`

## v0.1.2.dev6 (15/06/2022)

- bug fix in `BaseSolver._assign_options`
- `BaseProblem.model_covariance_inv` and `BaseProblem.model_covariance`

## v0.1.2.dev5 (09/06/2022)

- `BaseProblem.set_data_covariance` and more general linear system solver

## v0.1.2.dev4 (07/06/2022)

- bugs fix in `EmceeSolver` and result summary

## v0.1.2.dev3 (06/06/2022)

- bug fixed in `BaseProblem.set_regularisation`

## v0.1.2.dev2 (03/06/2022)

- Added `emcee` as new solver, with the following new APIs
  - `BaseProblem.set_log_prior`
  - `BaseProblem.set_log_likelihood`,
  - `BaseProblem.set_log_posterior`,
  - `BaseProblem.set_log_posterior_with_blobs`,
  - `BaseProblem.set_blobs_dtype`
- Process sampler output by converting to `arviz.InferenceData`, with the new API:
  - class `SamplingResult`
  - `SamplingResult.to_arviz()`
- Removed `BaseProblem.set_dataset(x,y)`, added `BaseProblem.set_data(y)`
- Added args and kwargs for all setting functions in `BaseProblem`
  - `_FunctionWrapper`
- Relaxed python version `>=3.8` to `>=3.6`
- Docs improvement, updated with emcee

## v0.1.2.dev1 (16/05/2022)

- bug fixes

## v0.1.2.dev0 (13/05/2022)

- `InversionRunner` has been changed into `Inversion`
- Added a references list for each backend tool
- How much information in `BaseProblem` is used for the inversion run
  now displayed through `Inversion.summary()`
- `numpy` and `scipy` versions relaxed
- Set objective function to be equal to data misfit if regularisation
  is not set
- Better error message when building failed
